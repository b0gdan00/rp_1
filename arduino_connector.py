import serial
import json
import time
import threading
import glob
import sys

class ArduinoSerial:
    def __init__(self, port=None, baud_rate=9600, timeout=1):
        """Initialize the connection with Arduino, automatically detecting the port if not provided."""
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.port = port if port else self.find_arduino_port()

        if not self.port:
            raise ValueError("Arduino port not found!")

        try:
            self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
            time.sleep(2)  # Wait for serial initialization
            print(f"Connected to Arduino on {self.port}")
        except serial.SerialException as e:
            raise RuntimeError(f"Failed to open serial port {self.port}: {e}")

    @staticmethod
    def find_arduino_port():
        """Automatically detect the Arduino port on Linux or Windows."""
        print(f"Detecting Arduino on {sys.platform}...")

        if sys.platform.startswith('linux'):
            return "/dev/ttyUSB0"
        elif sys.platform.startswith('win'):

            return "COM3" 
        else:
            return None  # Unsupported system

        for port in ports:
            try:
                with serial.Serial(port, 9600, timeout=1) as ser:
                    time.sleep(1)  # Wait for device response
                    ser.write(b'{"command":"ping"}\n')
                    response = ser.readline().decode().strip()
                    if "pong" in response:  # Expecting Arduino to respond with "pong"
                        return port
            except (OSError, serial.SerialException):
                continue

        return None

    def send_command(self, command, value=0):
        """Send a JSON command to Arduino."""
        try:
            data = json.dumps({"command": command, "value": value}) + "\n"
            self.ser.write(data.encode())
            print(f"Sent: {data.strip()}")
        except serial.SerialException as e:
            print(f"Error sending command: {e}")

    def listen(self):
        """Continuously listen to the serial port and receive data from Arduino."""
        while True:
            try:
                if self.ser.in_waiting > 0:
                    response = self.ser.readline().decode().strip()
                    if response:
                        try:
                            data = json.loads(response)
                            print(f"Received: {data}")
                        except json.JSONDecodeError:
                            print(f"Decoding error: {response}")
            except serial.SerialException as e:
                print(f"Serial error: {e}")
                break

    def start_listener(self):
        """Start the listener in a separate thread."""
        listener_thread = threading.Thread(target=self.listen, daemon=True)
        listener_thread.start()

    def get_response(self):
        """Synchronously read the response from Arduino (useful for data requests)."""
        time.sleep(1)  # Give Arduino time to send a response
        if self.ser.in_waiting > 0:
            response = self.ser.readline().decode().strip()
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {"error": "Decoding error", "data": response}
        return None

    def close(self):
        """Close the serial connection properly."""
        if self.ser.is_open:
            self.ser.close()
            print("Serial connection closed.")
