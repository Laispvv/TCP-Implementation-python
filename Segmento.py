import struct
import array
import socket

# def checksum(segmento: bytes) -> int:
#     if len(segmento) % 2 != 0:
#         segmento += b'\0'
#     res = sum(array.array("H", segmento))
#     res = (res >> 16) + (res & 0xffff)
#     res += res >> 16
#     return (~res) & 0xffff

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
                 flags,
                 seq_number,
                 ack_number,
                 ack_flag,
                 tam_header,
                 janela,
                 checksum,
                 data = 0
                 ):
        self.host_origem        = host_origem
        self.host_destino       = host_destino
        self.port_origem        = port_origem
        self.port_destino       = port_destino
        self.flags              = flags
        self.seq_number         = seq_number
        self.ack_number         = ack_number
        self.ack_flag           = ack_flag
        self.tam_header         = tam_header
        self.janela             = janela
        self.checksum           = checksum
        self.data               = data
    
    def build(self) -> bytes:
        # segmento = struct.pack(
        #     self.host_origem , 
        #     self.host_destino,
        #     self.port_origem ,
        #     self.port_destino,
        #     self.flags       ,
        #     self.seq_number  ,
        #     self.ack_number  ,
        #     self.ack_flag    ,
        #     self.tam_header  ,
        #     self.janela      ,
        #     self.checksum    ,
        #     self.data        
        # )
        teste = f"{self.host_origem},{self.port_origem},{self.host_destino},{self.port_destino},{self.flags},{self.seq_number},{self.ack_number},{self.ack_flag},{self.tam_header},{self.janela},{self.checksum},{self.data}"
        # header = struct.pack(
        #     '!4s4sHH',
        #     socket.inet_aton(self.host_origem),
        #     socket.inet_aton(self.host_destino),
        #     socket.SOCK_DGRAM,
        #     len(segmento)
        # )
        # teste2 = f"!4s4sHH, {socket.inet_aton(self.host_origem)}, {socket.inet_aton(self.host_destino)}, {socket.SOCK_DGRAM},{len(segmento)}"
        # cksum = checksum(header + segmento)
        # cksumfake = checksumfake(teste + teste2)
        cksumfake = checksumfake(teste)
        # segmento = segmento[:16] + struct.pack('H', cksum) + segmento[18:]
        testefinal = f"{teste[:45]}{cksumfake},{teste[47:]}"
        print(testefinal)
    
        #return segmento
        return bytes(testefinal, encoding='utf-8')
        
        