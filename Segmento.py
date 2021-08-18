import struct
import array
import socket

class Segmento:
    def __init__(self,
                 host_origem,
                 port_origem,
                 host_destino,
                 port_destino,
                 flags = 0
                 ):
        self.host_origem = host_origem
        self.host_destino = host_destino
        self.port_origem = port_origem
        self.port_destino = port_destino
        self.flags = flags
    
    def build(self):
        segmento = struct.pack(
            '!HHIIBBHHH',
            self.port_origem,
            self.port_destino,
            0,
            0,
            5 << 4,
            self.flags,
            8192,
            0,
            0,            
        )
        header = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.host_origem),
            socket.inet_aton(self.host_destino),
            socket.SOCK_DGRAM,
            len(segmento)
        )
        
        checksum = checksum(header + segmento)
        segmento = segmento[:16] + struct.pack('H', checksum) + segmento[18:]
    
        return segmento
    
    def checkSum(segmento):
        if len(segmento) % 2 != 0:
            segmento += b'\0'
        res = sum(array.array("H", segmento))
        res = (res >> 16) + (res & 0xffff)
        res += res >> 16
        return (~res) & 0xffff
        
        