import serial
import time
import struct
import logging
import variensevmu.messages as messages


class VMU931Parser(object):

    def __init__(self, device="/dev/tty.usbmodem1411"):
        """
        Opens connection to VMU931 device
        :param device: 
        """
        self.ser = serial.Serial(device)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.ser.close()

    def toggle_quaternion(self):
        """
        Toggles quaternion output from the VMU931 device
        :return: 
        """
        self.send_message("varq")

    def toggle_euler(self):
        """
        Toggles quaternion output from the VMU931 device.
        :return: 
        """
        self.send_message("vare")

    def toggle_heading(self):
        """
        Toggles heading output from the VMU931 device.
        :return: 
        """
        self.send_message("varh")

    def toggle_accelerometer(self):
        """
        Toggles accelerometer output from the VMU931 device.
        :return: 
        """
        self.send_message("vara")

    def toggle_gyroscope(self):
        """
        Toggles gyroscope output from the VMU931 device.
        :return: 
        """
        self.send_message("varg")

    def toggle_magnetometer(self):
        """
        Toggles magnetometer output from the VMU931 device.
        :return: 
        """
        self.send_message("varc")

    def set_gyroscope_resolution(self, resolution):
        """
        Sets the gyroscope output resolution of the VMU931 device.
        :param resolution: 250, 500, 1000 or 2000.
        :return: 
        """
        assert resolution in (250, 500, 1000, 2000), "Invalid gyroscope resolution, must be 250, 500, 1000 or 2000"

        mapping = {250: 0, 500: 1, 1000: 2, 2000: 3}
        command = "var{}".format(mapping[resolution])
        self.send_message(command)

    def set_accelerometer_resolution(self, resolution):
        """
        Sets the accelerometer output resolution of the VMU931 device.
        :param resolution: 2, 4, 8 or 16. 
        :return: 
        """
        assert resolution in (2, 4, 8, 16), "Invalid accelerometer resolution, must be 2, 4, 8 or 18"

        mapping = {2: 4, 4: 5, 8: 6, 16: 7}
        command = "var{}".format(mapping[resolution])
        self.send_message(command)

    def send_message(self, message):
        """
        Sends a message to the VMU931 device, with 5ms delay between each character.
        :param message: 
        :return: 
        """
        bmessage = message.encode('ascii')

        # bytes must be sent with 1ms+ interval to be recognised by device.
        for c in bmessage:
            bs = bytes([c])
            self.ser.write(bs)
            logging.debug("Sent {}".format(bs))
            time.sleep(0.005)

    def parse(self, callback=None):
        """
        Parses a single packet from the VMU931 device, returning a namedtuple. Typically called multiple times from
         within a loop.
        :param callback: Method to call after processing each packet
        :return: 
        """

        # Find start of data message -- we might start processing data mid-stream so need to synchronise.
        # We are looking for the magic byte 0x01. There's a chance that this will be randomly encountered, but
        # we also check the footer value.
        message_start = self.ser.read()[0]
        while message_start != 0x01:
            logging.debug("Skipping invalid message_start, got {} expected 0x01".format(hex(message_start)))
            message_start = self.ser.read()[0]
            continue

        message_size = self.ser.read()[0] - 4  # Unsure why we have to subtract 4bytes from this... but we do.
        logging.debug("Message size: {}".format(message_size))
        message_type = chr(self.ser.read()[0])
        logging.debug("Message type: {}".format(message_type))
        message_text = self.ser.read(message_size)
        message_end = self.ser.read()[0]

        if message_end != 0x04:
            logging.warning("Invalid Message footer (was {}, expected 0x04), skipping this packet".format(message_end))
            return

        if message_type == 'e':
            logging.info("Parsing Euler")
            data = VMU931Parser.parse_euler(message_text)
        elif message_type == 'q':
            logging.info("Parsing Quaternion")
            data = VMU931Parser.parse_quaternion(message_text)
        elif message_type == 'h':
            logging.info("Parsing Heading")
            data = VMU931Parser.parse_heading(message_text)
        elif message_type == 'a':
            logging.info("Parsing Accelerometer")
            data = VMU931Parser.parse_accelerometer(message_text)
        elif message_type == 'g':
            logging.info("Parsing Gyroscope")
            data = VMU931Parser.parse_gyroscope(message_text)
        elif message_type == 'c':
            logging.info("Parsing Magnetometer")
            data = VMU931Parser.parse_magnetometer(message_text)
        else:
            logging.warning("No parser for {}".format(message_type))
            return

        if callback is not None and data is not None:
            callback(data)

        return data

    @staticmethod
    def parse_quaternion(data):
        ts, w, x, y, z = struct.unpack(">Iffff", data[:20])
        return messages.Quaternion(timestamp=ts, w=w, x=x, y=y, z=z)

    @staticmethod
    def parse_euler(data):
        ts, x, y, z = struct.unpack(">Ifff", data[:16])
        return messages.Euler(timestamp=ts, x=x, y=y, z=z)

    @staticmethod
    def parse_accelerometer(data):
        ts, x, y, z = struct.unpack(">Ifff", data[:16])
        return messages.Accelerometer(timestamp=ts, x=x, y=y, z=z)

    @staticmethod
    def parse_magnetometer(data):
        ts, x, y, z = struct.unpack(">Ifff", data[:16])
        return messages.Magnetometer(timestamp=ts, x=x, y=y, z=z)

    @staticmethod
    def parse_gyroscope(data):
        ts, x, y, z = struct.unpack(">Ifff", data[:16])
        return messages.Gyroscope(timestamp=ts, x=x, y=y, z=z)

    @staticmethod
    def parse_heading(data):
        ts, h = struct.unpack(">If", data[:8])
        return messages.Heading(timestamp=ts, h=h)


if __name__ == "__main__":

    with VMU931Parser() as vp:

        #vp.toggle_euler()
        #vp.toggle_quaternion()
        #vp.toggle_accelerometer()
        #vp.toggle_gyroscope()
        #vp.toggle_heading()
        #vp.toggle_magnetometer()

        for n in range(10000):
            vp.parse(callback=print)
