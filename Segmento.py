import struct
import array
import socket
from Functions import *


def checksum1(segmento):
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
                 syn,
                 fin,
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
        self.syn                = syn
        self.fin                = fin
    
    def build(self) -> bytes:
        segmento = {
            "ip_origem": self.host_origem,
            "port_origem": self.port_origem,
            "ip_destino": self.host_destino,
            "port_destino": self.port_destino,
            "flags": self.flags,
            "seq": self.seq_number,  
            "ack": self.ack_number,  
            "ack_flag": self.ack_flag,
            "tam_header": self.tam_header,
            "janela": self.janela,
            "syn": self.syn,
            "fin": self.fin,
            "seq_number": self.seq_number,
            "ack_number": self.ack_number,
            "data": self.data
            # mss
        }
        segmento_string = destroy_dict(segmento)
        cksum = checksum1(segmento_string)
        segmento["checksum"] = cksum
        segmento_string = destroy_dict(segmento)
    
        return bytes(segmento_string, encoding='utf-8')
    
    def set_data(self, data):
        self.data = data

    def clone(self):
        return Segmento(self.host_origem, self.port_origem, self.host_destino, self.port_destino, self.flags, self.syn, self.fin, self.seq_number, self.ack_number, self.ack_flag, self.tam_header, self.janela, self.checksum, self.data)
        