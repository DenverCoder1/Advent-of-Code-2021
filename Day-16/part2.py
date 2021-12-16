"""
--- Part Two ---
Now that you have the structure of your transmission decoded, you can calculate the value of the expression it represents.

Literal values (type ID 4) represent a single number as described above. The remaining type IDs are more interesting:

Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
Using these rules, you can now work out the value of the outermost packet in your BITS transmission.

For example:

C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
04005AC33890 finds the product of 6 and 9, resulting in the value 54.
880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
D8005AC2A8F0 produces 1, because 5 is less than 15.
F600BC2D8F produces 0, because 5 is not greater than 15.
9C005AC2F8F0 produces 0, because 5 is not equal to 15.
9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?
"""

import os
from dataclasses import dataclass
from functools import reduce


@dataclass
class Packet:
    """
    Base class for all packets
    """

    version: int
    packet_type: int

    @abstractmethod
    def value(self) -> int:
        """Return the value of the packet"""
        pass

    def __int__(self):
        return self.value()


@dataclass
class LiteralValuePacket(Packet):
    """
    Class for literal value packets
    """

    __value: int

    @property
    def value(self) -> int:
        """For a literal value packet, just return the value"""
        return self.__value


@dataclass
class OperatorPacket(Packet):
    """
    Class for operator packets
    """

    subpackets: list[Packet]

    @property
    def value(self) -> int:
        """For an operator packet, return the value of the operation"""
        if self.packet_type == 0:
            return sum(subpacket.value for subpacket in self.subpackets)
        if self.packet_type == 1:
            return reduce(lambda x, y: x * y, (p.value for p in self.subpackets))
        if self.packet_type == 2:
            return min(subpacket.value for subpacket in self.subpackets)
        if self.packet_type == 3:
            return max(subpacket.value for subpacket in self.subpackets)
        if self.packet_type == 5:
            return 1 if self.subpackets[0].value > self.subpackets[1].value else 0
        if self.packet_type == 6:
            return 1 if self.subpackets[0].value < self.subpackets[1].value else 0
        if self.packet_type == 7:
            return 1 if self.subpackets[0].value == self.subpackets[1].value else 0
        raise ValueError(f"Unknown packet type: {self.packet_type}")


class Bits:
    """
    Class to represent a binary string of 1's and 0's and parse it into packets.
    """

    def __init__(self, bit_string: str):
        """
        Constructor

        Args:
            bit_string (int): A string of 1's and 0's to parse
        """
        self.data = bit_string

    def parse_packet(self) -> tuple[Packet, "Bits"]:
        """
        Parse the bits as a packet.

        Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        Packets with type ID 1 are product packets - their value is the result of multiplying together the values of their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
        Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
        Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
        Packets with type ID 4 are literal value packets - their value is the number represented by the packet.
        Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
        Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.

        Returns:
            A tuple containing the parsed packet and the remaining bits.
        """
        data = self.data
        version = int(data[0:3], 2)
        packet_type = int(data[3:6], 2)
        if packet_type == 4:
            num = ""
            for i in range(6, len(data), 5):
                num += data[i + 1 : i + 5]
                if data[i] == "0":
                    break
            value = int(num, 2)
            return Packet(version, packet_type, value), Bits(data[i + 5 :])
        length_type = data[6]
        subpackets = []
        if length_type == "0":
            # next 15 bits are a number that represents the total length in bits of the sub-packets contained by this packet
            length = int(data[7:22], 2)
            subpacket_bits = Bits(data[22 : 22 + length])
            while subpacket_bits.data:
                subpacket, subpacket_bits = subpacket_bits.parse_packet()
                subpackets.append(subpacket)
            data = data[22 + length :]
        else:
            # next 11 bits are a number that represents the number of sub-packets immediately contained by this packet
            length = int(data[7:18], 2)
            data = data[18:]
            for i in range(0, length):
                subpacket, bits = Bits(data).parse_packet()
                subpackets.append(subpacket)
                data = bits.data

        return OperatorPacket(version, packet_type, subpackets), Bits(data)

        return Packet(version, packet_type, value), Bits(data)

    def __repr__(self):
        return self.data

    @classmethod
    def from_hex(cls, hex_string: str) -> "Bits":
        """
        Convert a hex string to binary and left-pad with zeroes to make it a multiple of 4 bits

        Args:
            hex_string (str): A hex string to convert to binary
        """
        return cls(bin(int(hex_string, 16))[2:].zfill(len(hex_string) * 4))


def main():
    with open(os.path.join(os.path.dirname(__file__), "input.txt")) as f:
        data = f.read()

    bits = Bits.from_hex(data)

    print(f"The value of the packet is {bits.parse_as_packet().value}")


if __name__ == "__main__":
    main()
