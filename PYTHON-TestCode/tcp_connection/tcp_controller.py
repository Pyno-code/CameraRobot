

from queue import Queue
import time
import traceback
from bluetooth_connection.constants import IP_UUID, PORT_UUID
from tcp_connection.client import Client


class TCPController:
    def __init__(self, running, queue_logger: Queue, queue_send_tcp_message: Queue, queue_recv_tcp_message: Queue, order_dict: dict, dict_values: dict) -> None:
        self.queue_logger = queue_logger
        self.queue_send_tcp_message = queue_send_tcp_message
        self.queue_recv_tcp_message = queue_recv_tcp_message
        self.order_dict = order_dict
        self.dict_values = dict_values
        self.running = running

        self.start_ping = time.time()

        self.client = None

    def start(self):
        self.loop()

    def loop(self):
        time.sleep(1)
        while self.running.value:
            try:
                # TODO: RECONNEXION AU SERVER APRES DECONNEXION
                if self.order_dict["TCP_CONNECTION"] == "true":
                    if not self.is_connected():
                        self.queue_logger.put(('INFO', "Trying to connect to the tcp server"))
                        self.queue_logger.put(('INFO', f"Server at {self.dict_values[IP_UUID]}:{self.dict_values[PORT_UUID]}"))
                        self.client = Client()
                        self.client.connect((str(self.dict_values[IP_UUID]), int(self.dict_values[PORT_UUID])))
                        time.sleep(3)
                        self.dict_values["TCP_CONNECTED"] = "true" if self.is_connected() else "false"

                        if self.is_connected():
                            self.queue_logger.put(('SUCCESS', "Connected to the tcp server "))
                            self.queue_logger.put(("SUCCESS", "at " + str(self.dict_values[IP_UUID]) + ":" + str(self.dict_values[PORT_UUID]))) 
                        else:
                            self.queue_logger.put(('WARNING', "Failed to connect to the tcp server"))
                    else:
                        if self.order_dict["TCP_UPDATE"] == "true":
                            
                            self.client.receive()
                            if self.client.has_message():
                                message = self.client.get_message()
                                list_args_message = message.split("|")
                                if list_args_message[0] == "ping":
                                    self.queue_logger.put(('INFO', f"Ping : {(round(time.time(), 5) - eval(list_args_message[1]))/2}" ))
                                else:
                                    self.queue_logger.put(('INFO', f"Received message : {message}"))
                                    self.queue_recv_tcp_message.put(message)
                            
                            for i in range(self.queue_send_tcp_message.qsize()):
                                message = self.queue_send_tcp_message.get()
                                if message == "ping":
                                    self.start_ping = time.time()
                                    self.client.send(f"ping|{str(round(time.time(), 5))}$")
                                else:
                                    self.client.send(message+"$")
                                self.queue_logger.put(('INFO', f"Sent message : {message}"))
                                self.queue_send_tcp_message.task_done()
                            

                else:           
                    if self.is_connected():
                        self.client.close()
                        self.dict_values["TCP_CONNECTED"] = "false"

            except Exception as e:
                traceback_str = traceback.format_exc()
                self.queue_logger.put(('ERROR',  traceback_str))
                print(traceback_str)

                if self.is_connected():
                    self.client.close()
                    self.dict_values["TCP_CONNECTED"] = "false"

    def is_connected(self):
        if self.client is not None:
            return self.client.is_connected()
        return False

    def stop(self):
        pass

    