import datetime
import serial
import struct

from enum import Enum


class NsrtMk3Dev:
    """
    This class provides access to all the NSRT mk3 Dev API as published in the datasheet
    """
    ACK = 0x06
    SECONDS_FROM_1904_TO_1970 = 2082844800

    class Weighting(Enum):
        """
        Enumeration class for the weighting selection
        """
        #: DB_C
        DB_C = 0

        #: DB_A
        DB_A = 1

        #: DB_Z
        DB_Z = 2

    def __init__(self, port: str):
        """Initialise the NSRT mk3 Dev class

        Args:
            port: Virtual commport that was assigned to the NSRT by the OS (eg: COM12, /dev/ttyACM0)
        """
        self.serial = serial.Serial(port=port)

    def _command_reply(self, command: int, address: int, count: int, data=[]) -> bytearray:
        """Private function for sending the commands and reveing the reply. Used by the API functions to reduce boiler
        plating.

        Args:
            command: The command indicates the data transmitted or operation performed. The indicated direction
                     of transmission is host-centric.
                     Bit 31 of the command word indicates the direction of transfer:
                     0: OUT (Host to Device)
                     1: IN (Device to Host)
            address: The function of the address field varies with the command
            count: This field indicates the number of bytes to be transferred in the following data packet
                   (either an IN or an OUT). How the bytes are interpreted is defined by the command.
                   This number DOES NOT INCLUDE the command packet.
            data: Data Packets are simply a concatenation of bytes. The way the bytes are interpreted is a
                  function of the command that precedes the Data packet.
        Returns:
            The Ack is a single byte with value 0x06. The Ack byte is only sent back to the host if the command
            is a Write, and therefore does not require a data response from the device. When the command is a
            Read, the actual data sent back to the host serves that purpose
        """
        packed_data = list(struct.pack('<LLL', command, address, count)) + list(data)

        self.serial.write(packed_data)

        return self.serial.read(count if (command & 0x80000000) == 0x80000000 else 1)

    def read_level(self) -> float:
        """This command retrieves the current running level in dB. That is an exponentially averaged level, using the time
        constant and weighting function set for the instrument. That is not an LEQ.

        Returns:
            level in dB
        """
        reply = self._command_reply(0x80000010, 0, 4)

        return struct.unpack('<f', reply)[0]

    def read_leq(self) -> float:
        """This command retrieves the current running LEQ and starts the integration of a new LEQ. This way the next
        read_leq command returns the LEQ calculated between the present time and the retrieval of the previous LEQ.

        Returns:
            level in dB
        """
        reply = self._command_reply(0x80000011, 0, 4)

        return struct.unpack('<f', reply)[0]

    def read_temperature(self) -> float:
        """This command retrieves the temperature

        Returns:
            Float representing the temperature in degC
        """
        reply = self._command_reply(0x80000012, 0, 4)

        return struct.unpack('<f', reply)[0]

    def read_weighting(self) -> Weighting:
        """This command returns the weighting curve that is currently selected

        Returns:
            Weighting curve: DB_C / DB_A / DB_Z
        """
        reply = self._command_reply(0x80000020, 0, 1)

        return self.Weighting(reply[0])

    def write_weighting(self, weighting: Weighting) -> bool:
        """This command selects the weighting curve

        Args:
           Weighting curve: DB_C / DB_A / DB_Z

        Returns:
            True if succeeded otherwise False
        """
        reply = self._command_reply(0x00000020, 0, 1, [weighting.value])

        return reply[0] == self.ACK

    def read_fs(self) -> int:
        """This command reads the current sampling frequency

        Returns:
            Sampling frequency in Hz
        """
        reply = self._command_reply(0x80000021, 0, 2)

        return struct.unpack('<H', reply)[0]

    def write_fs(self, frequency: int):
        """This command sets the sampling frequency

        Args:
            Sampling frequency in Hz

        Returns:
            True if succeeded otherwise False

        Raises:
            ValueError: if the given frequency is invalid
        """
        if not ((frequency == 32000) or (frequency == 48000)):
            raise ValueError(f'{frequency} not supported. Value can only be 32000 or 48000')

        reply = self._command_reply(0x00000021, 0, 1, struct.pack('<H', frequency))

        return reply[0] == self.ACK

    def read_tau(self) -> float:
        """This command reads the current time constant

        Returns:
            Float representing the time constant in s.
        """
        reply = self._command_reply(0x80000022, 0, 4)

        return struct.unpack('<f', reply)[0]

    def write_tau(self, tau: float):
        """This command sets the time constant

        Args:
            tau: Float representing the time constant in s.

        Returns:
            True if succeeded otherwise False
        """
        reply = self._command_reply(0x00000022, 0, 1, struct.pack('<f', tau))

        return reply[0] == self.ACK

    def read_model(self):
        """This command reads the model

        Returns:
            ASCII string representing the Model
        """
        reply = self._command_reply(0x80000031, 0, 32)

        return reply.decode('utf-8').split('\x00')[0]

    def read_sn(self):
        """This command reads the serial number

        Returns:
            ASCII string representing the serial number of the instrument.
        """
        reply = self._command_reply(0x80000032, 0, 32)

        return reply.decode('utf-8').split('\x00')[0]

    def read_fw_rev(self):
        """This command reads the fw revision

        Returns:
            ASCII string representing the Firmware revision
        """
        reply = self._command_reply(0x80000033, 0, 32)

        return reply.decode('utf-8').split('\x00')[0]

    def read_doc(self) -> datetime.datetime:
        """This command reads the date of calibration

        Returns:
            UTC datetime object representing the calibration date
        """
        reply = self._command_reply(0x80000034, 0, 8)

        return datetime.datetime.fromtimestamp(struct.unpack('<Q', reply)[0] - self.SECONDS_FROM_1904_TO_1970).strftime('%Y-%m-%d %H:%M:%S')

    def read_dob(self) -> datetime.datetime:
        """This command reads the date of birth

        Returns:
            UTC datetime object representing the manufacturing date
        """
        reply = self._command_reply(0x80000035, 0, 8)

        return datetime.datetime.fromtimestamp(struct.unpack('<Q', reply)[0] - self.SECONDS_FROM_1904_TO_1970).strftime('%Y-%m-%d %H:%M:%S')

    def read_user_id(self):
        """This command reads the user id

        Returns:
            ASCII string representing the UserID, as defined by the user.
        """
        reply = self._command_reply(0x80000036, 0, 32)

        return reply.decode('utf-8').split('\x00')[0]

    def write_user_id(self, user_id):
        """This command sets the user id

        Returns:
            True if succeeded otherwise False

        Raises:
            ValueError: if the given string is longer than 31 characters
        """
        if len(user_id) >= 32:
            raise ValueError('Maximum length for the user id is 31 characters')

        zero_terminated_string = (user_id + '\x00').encode('utf-8')
        reply = self._command_reply(0x00000036, 0, len(zero_terminated_string), zero_terminated_string)

        return reply[0] == self.ACK
