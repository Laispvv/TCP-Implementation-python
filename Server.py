from time import sleep
from Segmento import Segmento
from socket import *
from VariaveisControle import *
from Functions import *

class Server:
    def __init__(self) -> None:
        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.tcp_handshake = False
    
    def criar_conexao(self):
        data, (ip, client_port) = self.connection.recvfrom(MSS)
        dicionario = build_dict(str(data, encoding='utf-8'))
        if(dicionario["syn"] == '1'):
            buffer = [0 for i in range(int(dicionario["janela"]))]
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
        
# PROXIMO PASSSO: DIVIDIR ARQUIVO EM SEGMENTOS
# DEPOIS DISSO: COMO ENVIAR E RECEBER ACKS
# AI DEPOIS: O SLOW-START
# E ENTÃO: O FAST-RECOVERY CONGESTÃO
# E POR FIM: TIME-OUT

    def start_server(self):
        self.connection.bind(('', port))
        print("Servidor de pé e ouvindo")

        # ouvindo possíveis datagramas que podem chegar
        while(True):
            self.criar_conexao()
            while not self.tcp_handshake:
                sleep(2)
            data, (ip, client_port) = self.connection.recvfrom(MSS)
            print(data)
            text = str(data, 'utf-8')
            print("O Cliente em {}:{} enviou {}".format(ip, client_port, text))
            
            # enviando uma resposta para o cliente
            msg = "OK - enviou " + str(data, 'utf-8')
            msg = "data: dados aqui, SYN:1"
            self.connection.sendto(bytes(msg, encoding='utf8'), (ip, client_port))
        
if __name__ == '__main__':
    servidor = Server()
    servidor.start_server()






