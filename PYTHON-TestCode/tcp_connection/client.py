import socket
from threading import Thread
import time
from multiprocessing import Manager, Queue
from test import *


class Client:

    def __init__(self, debug=False) -> None:
        self.debug = debug
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_initialized = False
        self.socket.settimeout(3)

        self.message_queue: Queue = Queue()

        self.connected = Manager().Value('b', False)
        self.receive_process: Thread = Thread(target=self.receive_, args=(self.message_queue, self.connected))

        self.closed = False


    def connect(self, address: tuple[str, int]) -> None:
        if not self.socket_initialized:
            try:
                if self.debug:
                    print('Tentative de connexion au serveur :', address)
                self.socket.connect(address)
                self.connected.value = True
                if self.debug:
                    print('Connecté au serveur :', address)
                self.socket_initialized = True
                return True
            except ConnectionRefusedError:
                if self.debug:
                    print('Impossible de se connecter au serveur')
                return False
            except socket.timeout:
                if self.debug:
                    print('Connexion au serveur impossible : timeout')
                return False
            except OSError:
                self.__init__(self.debug)
                return self.connect(address)
        else:
            self.__init__(self.debug)
            self.connect(address)

    
    def send(self, data: bytes) -> None:
        if self.is_connected():
            send_process = Thread(target=self.send_, args=(data, self.connected))
            send_process.start()
        

    def send_(self, data: bytes, connected) -> None:
        try:
            self.socket.sendall(data)
            if self.debug:
                print('Message envoyé au serveur')
        except ConnectionResetError:
            connected.value = False
            if self.debug:
                print("ConnectionResetError", 'Connexion perdue avec le serveur')

        except ConnectionAbortedError:
            self.connected.value = False
            if self.debug:
                print("ConnectionAbortedError", 'Connexion perdue avec le serveur')
    
    def receive(self) -> str:
        if self.is_connected():
            if not self.receive_process.is_alive():
                self.receive_process = Thread(target=self.receive_, args=(self.message_queue, self.connected))
                self.receive_process.start()

    def receive_(self, message_queue: Queue, connected):
        try:
            message = self.socket.recv(1024).decode('utf-8')
            
            if self.debug:
                print(message)
            if message != '':
                message_queue.put(message)
            else:
                print('ConnectionError', 'Connexion perdue avec le serveur')
        except socket.timeout:
            pass
        except socket.error:
            connected.value = False
            if self.debug:
                print('ConnectionError', 'Connexion perdue avec le serveur')

    def has_message(self) -> bool:
        return not self.message_queue.empty()

    def get_message(self) -> bytes:
        if self.has_message():
            return self.message_queue.get()
        return None

    def is_connected(self):
        try:
            self.socket.getpeername()
        except socket.error:
            return False
        return self.connected.get()

    def get_address_server(self) -> tuple[str, int]:
        if self.is_connected():
            return self.socket.getpeername()

    def close(self):
        if self.receive_process is not None:
            try:
                self.receive_process.join()
            except RuntimeError:
                pass
        self.socket.close()
        self.message_queue.close()
        self.closed = True

def sending(client: Client):
    try:
        message = input('Message à envoyer : ').encode('utf-8')
        message = 0b0001000000000000.to_bytes(2, 'big')
        client.send(message)
        if message == 'exit':
            raise KeyboardInterrupt
    except EOFError:
        pass


if __name__ == '__main__':

    client = Client(True)
    sending_thread = Thread(target=sending, args=(client,))

    running = True
    while running:
        try:
            if client.is_connected():
                time.sleep(1)
                
                client.receive()
                if client.has_message():
                   client.get_message()

                if not sending_thread.is_alive():
                    sending_thread = Thread(target=sending, args=(client,))
                    sending_thread.start()
            else:
                time.sleep(1)
                client.connect(('192.168.11.108', 5000))
        except KeyboardInterrupt:
            running = False
        
        except EOFError:
            running = False

    client.close()
    print()
    print('Fermeture du client...')
