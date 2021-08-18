import struct
import array
import socket

def checksum(segmento: bytes) -> int:
    if len(segmento) % 2 != 0:
        segmento += b'\0'
    res = sum(array.array("H", segmento))
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff

def checksumfake(segmento):
    if len(segmento) % 2 != 0:
        segmento += '\0'
    res = 0
    for element in segmento:
        res += ord(element)
    
    res = (res >> 16) + (res & 0xffff)
    res += res >> 16
    return (~res) & 0xffff

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
    
    def build(self) -> bytes:
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
        teste = f"!HHIIBBHHH, {self.port_origem}, {self.port_destino}, 0, 0, 5 << 4, {self.flags}, 8192,0,0"
        header = struct.pack(
            '!4s4sHH',
            socket.inet_aton(self.host_origem),
            socket.inet_aton(self.host_destino),
            socket.SOCK_DGRAM,
            len(segmento)
        )
        teste2 = f"!4s4sHH, {socket.inet_aton(self.host_origem)}, {socket.inet_aton(self.host_destino)}, {socket.SOCK_DGRAM},{len(segmento)}"
        cksum = checksum(header + segmento)
        cksumfake = checksumfake(teste + teste2)
        segmento = segmento[:16] + struct.pack('H', cksum) + segmento[18:]
        testefinal = f"{teste[:16]}{cksumfake}{teste[18:]}"
    
        #return segmento
        return bytes(testefinal, encoding='utf-8')
        
        