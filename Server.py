from time import sleep
from Segmento import Segmento
from socket import *
from VariaveisControle import *
from Functions import *
from random import random

class Server:
    def __init__(self) -> None:
        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.tcp_handshake = False
        self.ack = 0
        self.seq = 0
        self.len_res = 0
        self.buffer = None
    
    def criar_conexao(self):
        data, (ip, client_port) = self.connection.recvfrom(MSS)
        dicionario = build_dict(str(data, encoding='utf-8'))
        if(dicionario["syn"] == '1'):
            self.buffer = [-1 for i in range(int(dicionario["janela"]))]
            segmento = Segmento(host_origem=host,
                                port_origem=port,
                                host_destino=host,
                                port_destino=port,
                                flags=0,
                                syn=1,
                                fin=0,
                                seq_number=numeroSequencia,
                                ack_number=int(dicionario["seq_number"]) + 1,
                                ack_flag=1,
                                tam_header=tamanhoHeader,
                                janela=janelaAtual,
                                checksum=0)
            self.connection.sendto(segmento.build(), (ip, client_port))
            data2, (ip2, client_port2) = self.connection.recvfrom(MSS)
            dicionario2 = build_dict(str(data2, encoding="utf-8"))
            if(int(dicionario2["ack_number"]) == numeroSequencia+1):
                # terminou o aperto de mão de 3 vias
                self.tcp_handshake = True
                print("Terminou o aperto de mão aqui também")
        
# PROXIMO PASSSO: DIVIDIR ARQUIVO EM SEGMENTOS check
# DEPOIS DISSO: COMO ENVIAR E RECEBER ACKS check
# AI DEPOIS: O SLOW-START
# E ENTÃO: O FAST-RECOVERY CONGESTÃO
# E POR FIM: TIME-OUT

    def start_server(self):
        file = open("output.txt", "w")
        self.connection.bind(('', port))
        print("Servidor de pé com ouvido")

        # ouvindo possíveis datagramas que podem chegar
        self.criar_conexao()
        while not self.tcp_handshake:
            sleep(2)

        while(True):
            data, (ip, client_port) = self.connection.recvfrom(MSS)
            dicionario = build_dict(str(data, encoding="utf-8"))

            if dicionario["fin"] == "1":
                break

            print("O Cliente em {}:{} enviou {}".format(ip, client_port, dicionario["data"]))
            file.write(dicionario["data"])
            
            # seq_number
            if (self.seq == 0):
                self.seq = random()
            else:
                self.seq += self.len_res
            

            # ack_number
            if (self.ack == 0):
                self.ack = dicionario["seq_number"]
            else:
                if (self.ack == dicionario["seq_number"]):  # aqui está errado a comparação
                    if self.buffer[0] != -1:
                        index = 0
                        while index < len(self.buffer):
                            if self.buffer[index] == -1:
                                break
                            self.ack += self.buffer[index]
                            self.buffer[index] = -1
                            index += 1
                    self.ack += dicionario["janela"]
                else:
                    index = 0
                    while index < len(self.buffer):
                        if self.buffer[index] != -1:
                            index += 1
                        else:
                            break
                    self.buffer[index] = dicionario["janela"]
                
            
            # enviando uma resposta para o cliente
            ack = Segmento(host_origem=host,
                                port_origem=port,
                                host_destino=host,
                                port_destino=port,
                                flags=0,
                                syn=0,
                                fin=0,
                                seq_number=self.seq,
                                ack_number=self.ack,
                                ack_flag=1,
                                tam_header=tamanhoHeader,
                                janela=0,       # tamanho dos dados enviados, no nosso caso, será sempre 0, pois estamos enviando apenas os acks (criar um novo atributo chamado len)
                                # tem que atualizar esse janela atual, dizendo quantos segmentos ainda podem ser enviados
                                checksum=0)
                            
            self.connection.sendto(ack.build(), (ip, client_port))

        self.connection.close()
        
if __name__ == '__main__':
    servidor = Server()
    servidor.start_server()






