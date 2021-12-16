from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from math import prod


class PacketType(IntEnum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


@dataclass
class Packet(ABC):
    version: int
    type_id: int

    def version_sum(self):
        return self.version

    @abstractmethod
    def value(self):
        ...


@dataclass(kw_only=True)
class LiteralPacket(Packet):
    val: int

    def value(self):
        return self.val


@dataclass(kw_only=True)
class OperatorPacket(Packet):
    subpackets: list[Packet]

    def version_sum(self):
        return self.version + sum(p.version_sum() for p in self.subpackets)

    def value(self):
        match self.type_id:
            case PacketType.SUM:
                return sum(p.value() for p in self.subpackets)
            case PacketType.PRODUCT:
                return prod(p.value() for p in self.subpackets)
            case PacketType.MINIMUM:
                return min(p.value() for p in self.subpackets)
            case PacketType.MAXIMUM:
                return max(p.value() for p in self.subpackets)
            case PacketType.GREATER_THAN:
                assert len(self.subpackets) == 2
                return 1 if self.subpackets[0].value() > self.subpackets[1].value() else 0
            case PacketType.LESS_THAN:
                assert len(self.subpackets) == 2
                return 1 if self.subpackets[0].value() < self.subpackets[1].value() else 0
            case PacketType.EQUAL_TO:
                assert len(self.subpackets) == 2
                return 1 if self.subpackets[0].value() == self.subpackets[1].value() else 0
            case _:
                return None


@dataclass
class BitString:
    def __init__(self, bitstring):
        self.bitstring = bitstring
        self.current_bit = 0

    def read_bitstring(self, size):
        val = self.peek(size)
        self.current_bit += size
        return val

    def read_int(self, size):
        return int(self.read_bitstring(size), 2)

    def read_packet(self):
        packet_version = self.read_int(3)
        packet_type_id = self.read_int(3)

        if packet_type_id == PacketType.LITERAL:
            literal_bits = []
            while True:
                prefix_bit = self.read_bitstring(1)
                group_bits = self.read_bitstring(4)

                literal_bits.append(group_bits)
                if prefix_bit == '0':
                    break

            return LiteralPacket(
                version=packet_version,
                type_id=packet_type_id,
                val=int(''.join(literal_bits), 2),
            )

        # Otherwise, it's an operator packet
        length_type_id = self.read_bitstring(1)

        if length_type_id == '0':
            total_length = self.read_int(15)

            subpackets = []
            starting_bit_read = self.current_bit
            current_bits_read = 0
            while current_bits_read < total_length:
                subpackets.append(self.read_packet())
                current_bits_read += (self.current_bit - starting_bit_read)
                starting_bit_read = self.current_bit

            return OperatorPacket(
                version=packet_version,
                type_id=packet_type_id,
                subpackets=subpackets,
            )
        elif length_type_id == '1':
            num_subpackets = self.read_int(11)
            subpackets = [self.read_packet() for _ in range(num_subpackets)]

            return OperatorPacket(
                version=packet_version,
                type_id=packet_type_id,
                subpackets=[p for p in subpackets if p],
            )

    def peek(self, size=1):
        if self.current_bit + size > len(self.bitstring):
            raise ValueError()

        return self.bitstring[self.current_bit:self.current_bit+size]

    def __len__(self):
        return len(self.bitstring)

    def __str__(self):
        return str(self.bitstring)


with open('input') as f:
    message = f.readline()

num_bits = len(message) * 4
message_bits = BitString(bin(int(message, 16))[2:].zfill(num_bits))
packet = message_bits.read_packet()
print(f'Part 1 solution: {packet.version_sum()}')
print(f'Part 2 solution: {packet.value()}')