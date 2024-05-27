from bluetooth_connection.constants import *


running = True

# ---------------
logger = None

FATAL = "FATAL"
ERROR = "ERROR"
WARNING = "WARNING"
INFO = "INFO"
DEBUG = "DEBUG"
# ---------------

bleValues = {
    IP_UUID : "192.168.0.4",
    PORT_UUID : "5000",
    SSID_UUID : "test",
    PASSWORD_UUID : "12345678",

    WIFI_STATUS_UUID : "false",
    WORKING_STATUS_UUID : "false",
    SERVER_TCP_STATUS_UUID : "false",

    ORDER_WIFI_CONNECTION_UUID : "false",
    ORDER_WORKING_UUID : "false"
}
