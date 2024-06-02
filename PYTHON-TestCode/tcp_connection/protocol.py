
from multiprocessing import Queue


STATUS = 0

PING = 1
MOTOR = 2
POSITION = 3

GET = 1
SET = 2
STOP = 3
START = 4
SHUTDOWN = 5

ANGLE = 6
SPEED = 7

ALL = 1
MOTOR_BASE = 2
MOTOR_MIDDLE = 3     
MOTOR_TOP = 4
MOTOR_X = 5
MOTOR_Y = 6
MOTOR_Z = 7


LIST_ARGS = [
    {
        "STATUS": STATUS,
        "PING": PING,
        "MOTOR": MOTOR,
        "POSITION": POSITION,
    },

    {
        "GET": GET,
        "SET": SET,
        "STOP": STOP,
        "START": START,
        "SHUTDOWN": SHUTDOWN,
        "ANGLE": ANGLE,
        "SPEED": SPEED,
    },

    {
        "ANGLE": ANGLE,
        "SPEED": SPEED,
    },

    {
        "*": ALL,
        "BASE": MOTOR_BASE,
        "MIDDLE": MOTOR_MIDDLE,
        "TOP": MOTOR_TOP,
        "X": MOTOR_X,
        "Y": MOTOR_Y,
        "Z": MOTOR_Z
    },
]

class Protocol:

    def __init__(self, queue_logger, queue_send_command: Queue, queue_send_tcp_message: Queue, queue_recv_tcp_message: Queue) -> None:
        self.queue_send_command = queue_send_command
        self.queue_send_tcp_message = queue_send_tcp_message
        self.queue_recv_tcp_message = queue_recv_tcp_message

        self.queue_logger = queue_logger

    def parse_command(self, message: str) -> dict:
        list_args = message.split(" ")
        return list_args
    
    def convert_command_to_list_int(self, message: str) -> list:
        list_args = self.parse_command(message)
        list_int = [0, 0, 0, 0]
        for i, arg in enumerate(list_args):
            list_int[i] = LIST_ARGS[i][arg]
        return list_int
    
    def convert_list_int_to_command(self, list_int: list) -> str:
        message = ""
        for i, arg in enumerate(list_int):
            for key, value in LIST_ARGS[i].items():
                if arg == value:
                    message += key + " "
        return message
    
    def convert_list_int_to_bytes(self, list_int: list) -> int:
        result = 0
        for i in range(len(list_int)):
            result = result | (list_int[i] << 4*(len(list_int)-1-i))
        return result
    
    def convert_bytes_to_list_int(self, byte: bytes) -> list:
        result = []
        for i in range(3, -1, -1):
            number = byte & (0b1111 << 4*i)
            number = number >> 4*i
            result.append(number)
        return result
    
    def convert_bytes_to_bytes_str(self, entier: int) -> None:
        binary_string = bin(entier)[2:].zfill(16)
        formatted_string = ' '.join([binary_string[i:i+4] for i in range(0, len(binary_string), 4)])
        return formatted_string
    
    def loop(self):
        for i in range(self.queue_send_command.qsize()):
            message = self.queue_send_command.get()

            list_int = self.convert_command_to_list_int(message)
            byte = self.convert_list_int_to_bytes(list_int)
            
            byte_str = self.convert_bytes_to_bytes_str(byte)
            self.queue_logger.put(('INFO', f"Command sended: {message}"))
            self.queue_logger.put(('INFO', f"Bytes sended: {byte_str}"))

            self.queue_send_tcp_message.put(bytes(byte))
        
        for i in range(self.queue_recv_tcp_message.qsize()):
            byte = self.queue_recv_tcp_message.get()
            byte_str = self.convert_bytes_to_bytes_str(byte)
            self.queue_logger.put(('INFO', f"Bytes recv: {byte_str}"))

            list_int = self.convert_bytes_to_list_int(byte)
            message = self.convert_list_int_to_command(list_int)
            self.queue_logger.put(('INFO', f"Command recv: {message}"))