import socket
from threading import Thread
import time
from multiprocessing import Manager, Queue


class Server:

    def __init__(self, port: int, debug=False) -> None:
        self.debug = debug
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.client: socket.socket = None
        
        self.message_queue: Queue = Queue()

        self.read_process: Thread = Thread(target=self.read_, args=(self.message_queue))
        self.listen_process: Thread = Thread(target=self.listen_)
    
    def connect(self):
        try:
            self.socket.bind((self.ip, self.port))
            if self.debug:
                print('Serveur démarré sur :', (self.ip, self.port))
        except socket.error:
            raise socket.error("Impossible de démarrer le serveur\nSerais-tu connecté à eduroam ?")
    def listen_(self):
        if self.client is None:
            if self.debug:
                print('Listening...')
            self.socket.listen(1)
            self.client, address = self.socket.accept()
            if self.client is not None:
                if self.debug:
                    print('Client connected :', address)
    
    def listen(self):
        if not self.listen_process.is_alive():
            self.listen_process = Thread(target=self.listen_)
            self.listen_process.start()
    
    def read_(self, queue: Queue) -> None:
        if self.client is not None:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message != '':
                    queue.put(message)
                else:
                    raise socket.error
                if self.debug:
                    print('Message received : *'+ message + '*')
            except socket.error:
                print('ConnectionError', 'Connexion perdue avec le client')
                self.client.close()
                self.client = None
    
    def read(self):
        if not self.read_process.is_alive():
            self.read_process = Thread(target=self.read_, args=(self.message_queue,))
            self.read_process.start()

    def send_(self, data: str) -> None:
        try:
            self.client.send(data.encode('utf-8'))
            if self.debug:
                print('Message sent to client')
        except socket.error:
            if self.debug:
                print('Connection lost with the client')
            self.client.close()
            self.client = None

    def send(self, data: str) -> None:
        if self.client is not None:
            send_process = Thread(target=self.send_, args=(data,))
            send_process.start()
    
    def get_message(self) -> str:
        if not self.message_queue.empty():
            return self.message_queue.get()
        return None
    
    def has_message(self) -> bool:
        return not self.message_queue.empty()
    
    def has_client(self) -> bool:
        return self.client is not None
    
    def close(self):
        if self.client is not None:
            self.client.close()
        self.socket.close()

if __name__ == '__main__':
    server = Server(5000, debug=True)
    connection = False
    while not connection:
        try:
            time.sleep(2)
            server.connect()
            connection = True
        except socket.error as e:
            print('connecté à eduroam ?')
            connection = False
    print('Server started')
    running = True
    try:
        while running:
            if not server.has_client():
                server.listen()
            else:
                server.read()
                if server.has_message():
                    message = server.get_message()
                    server.send('Message received')
                    if message.startswith('exit'):
                        raise KeyboardInterrupt

                
    except KeyboardInterrupt:
        server.close()
        running = False
        print('Server closed')