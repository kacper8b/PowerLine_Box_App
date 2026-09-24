
import serial
import sys
import _thread


class Uart:

    def __init__(self):
        """__init__
        ----------------------------------------------------------------------------------------------------------------
        """
        self.ReceiveCallback = None
        self.IsOpen = False
        self.SerialPort = serial.Serial()
        self.receivedMessage = None

    def connect(self, port="COM17", baud=38400):
        """connect
        ----------------------------------------------------------------------------------------------------------------
        """

        try:
            self.SerialPort = serial.Serial(port, baud, timeout=5)
            self.IsOpen = True
            return True
        except:
            print("Cant open specified port")
            self.IsOpen = False
            return False

    def disconnect(self):
        """disconnect
        ----------------------------------------------------------------------------------------------------------------
        """
        try:
            self.IsOpen = False
            self.SerialPort.close()
            return True
        except:
            print("Error")
            return False

    def register_new_thread(self, receive_callback, type_serial=0):
        """register_new_thread
        ----------------------------------------------------------------------------------------------------------------
        """
        self.ReceiveCallback = receive_callback

        try:
            if type_serial == 0:
                _thread.start_new_thread(self.serial_readline_thread, ())
            else:
                _thread.start_new_thread(self.serial_read_thread, ())
        except:
            print("Error starting Read thread: ", sys.exc_info()[0])

    def serial_readline_thread(self):
        """serial_readline_thread
        ----------------------------------------------------------------------------------------------------------------
        """
        while self.IsOpen:

            try:
                self.receivedMessage = self.SerialPort.readline()
                if self.receivedMessage != "":
                    self.ReceiveCallback(self.receivedMessage)
            except:
                print("Error reading line COM port: ")

    def change_callback(self, receive_callback):
        """change_callback
        ----------------------------------------------------------------------------------------------------------------
        """
        self.ReceiveCallback = receive_callback

    def serial_read_thread(self):
        """serial_read_thread
        ----------------------------------------------------------------------------------------------------------------
        """
        while self.IsOpen:
            try:
                self.receivedMessage = self.SerialPort.read()
                if self.receivedMessage != "":
                    self.ReceiveCallback(self.receivedMessage)
            except:
                print("Error reading COM port: ")

    def send_data(self, data):
        """send_data
        ----------------------------------------------------------------------------------------------------------------
        """
        if self.IsOpen:
            self.SerialPort.write(data)

    def is_open(self):
        """is_open
        ----------------------------------------------------------------------------------------------------------------
        """
        return self.IsOpen
