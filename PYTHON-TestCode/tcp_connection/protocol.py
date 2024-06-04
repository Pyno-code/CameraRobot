
import base64
from multiprocessing import Queue
import struct


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
        "_": 0
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
    
    def convert_command_to_list_int(self, list_args) -> list:
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
    
    def string_to_binary(self, s):
        return ' '.join(format(ord(char), '08b') for char in s)
    
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
    
    def float_to_binary64(self, value):
        return struct.pack('<d', value)
    
    def convert_list_float64_to_bytes(self, float_list: list) -> bytes:
        return [self.float_to_binary64(number) for number in float_list]
    
    def convert_list_float32_to_bytes(self, float_list: list) -> bytes:
        return [struct.pack('<f', number) for number in float_list] # little-endian base 32
    
    def loop(self):
        for i in range(self.queue_send_command.qsize()):
            message = self.queue_send_command.get()
            self.queue_logger.put(('INFO', f"Command : {message}"))
            list_args = self.parse_command(message)

            float_list = []
            for arg in list_args:
                try:
                    float_value = float(arg)
                    float_list.append(float_value)
                except ValueError:
                    pass
            str_list = [arg for arg in list_args if arg.isalpha()]
            str_list = [arg.upper() for arg in str_list]
            float_list.extend([0.0] * (6 - len(float_list)))

            list_int = self.convert_command_to_list_int(str_list)
            byte_command = self.convert_list_int_to_bytes(list_int)
            list_byte_arg = self.convert_list_float32_to_bytes(float_list)

            byte_args = b''.join(list_byte_arg)

            message_bytes = byte_command.to_bytes(2, 'big') + byte_args
            self.queue_logger.put(('DEBUG', f"LIST_COMMAND: {str_list}"))
            self.queue_logger.put(('DEBUG', f"LIST_FLOAT: {float_list}"))
            self.queue_logger.put(('DEBUG', f"COMMAND: {byte_command.to_bytes(2, 'big')}"))


            # self.queue_logger.put(('DEBUG', f"ARGS: {byte_args}"))
            # self.queue_logger.put(('DEBUG', f"MESSAGE: {message_bytes}"))
            # self.queue_logger.put(('DEBUG', f"Command sended: {message}"))

            # for e in list_byte_arg:
            #     unpacked_value = struct.unpack('<f', e)[0]
            #     binary_string = f'{unpacked_value}'
            #     self.queue_logger.put(('DEBUG', f'packed_value: {binary_string}'))

            
            byte_str = self.convert_bytes_to_bytes_str(byte_command)
            # self.queue_logger.put(('INFO', f"Command sended: {message}"))
            # self.queue_logger.put(('INFO', f"Bytes sended: {byte_str}"))
            self.queue_send_tcp_message.put(message_bytes)
        
        for i in range(self.queue_recv_tcp_message.qsize()):
            byte = self.queue_recv_tcp_message.get()
            byte_str = self.convert_bytes_to_bytes_str(byte)
            self.queue_logger.put(('INFO', f"Bytes recv: {byte_str}"))

            list_int = self.convert_bytes_to_list_int(byte)
            message = self.convert_list_int_to_command(list_int)
            self.queue_logger.put(('INFO', f"Command recv: {message}"))