from time import sleep
from Segmento import Segmento
from socket import *
from VariaveisControle import *
from Functions import *
from random import *
import Log

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
        # salvando resposta do cliente no log
        Log.ocorrido += f'\nO Cliente em {ip}:{client_port} enviou:\n'
        Log.ocorrido += f'Número de sequênica: {dicionario["seq_number"]}\t|\tSyn: {dicionario["syn"]}\t|\tTamanho do header: {dicionario["tam_header"]}\t|\tTamanho total: {dicionario["janela"]}\t|\tNúmero de confirmação: {dicionario["ack_number"]}\n'        
        Log.ocorrido += f'Dados: {dicionario["data"]}\n'   
                    
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
                                janela=0,
                                checksum=0)
            mensagem = segmento.build()
            segmento.tam_header = len(mensagem)
            
            self.connection.sendto(mensagem, (ip, client_port))
            dicionario = build_dict(str(mensagem, encoding="utf-8"))
            # salvando mensagem do servidor no log
            Log.ocorrido += f'\nO Servidor em {ip}:{host} enviou:\n'
            Log.ocorrido += f'Número de sequênica: {dicionario["seq_number"]}\t|\tSyn: {dicionario["syn"]}\t|\tTamanho do header: {dicionario["tam_header"]}\t|\tTamanho total: {dicionario["janela"]}\t|\tNúmero de confirmação: {dicionario["ack_number"]}\n'        
            Log.ocorrido += f'Dados: {dicionario["data"]}\n'   
            
            
            data2, (ip2, client_port2) = self.connection.recvfrom(MSS)
            dicionario2 = build_dict(str(data2, encoding="utf-8"))
            # salvando resposta do cliente no log
            Log.ocorrido += f'\nO Cliente em {ip2}:{client_port2} enviou:\n'
            Log.ocorrido += f'Número de sequênica: {dicionario2["seq_number"]}\t|\tSyn: {dicionario2["syn"]}\t|\tTamanho do header: {dicionario2["tam_header"]}\t|\tTamanho total: {dicionario2["janela"]}\t|\tNúmero de confirmação: {dicionario2["ack_number"]}\n'        
            Log.ocorrido += f'Dados: {dicionario2["data"]}\n'   
            
            if(int(dicionario2["ack_number"]) == numeroSequencia+1):
                # terminou o aperto de mão de 3 vias
                self.tcp_handshake = True
                print("Terminou o aperto de mão aqui também")
        
# PROXIMO PASSSO: DIVIDIR ARQUIVO EM SEGMENTOS check
# DEPOIS DISSO: COMO ENVIAR E RECEBER ACKS check
# AI DEPOIS: O SLOW-START check
# E ENTÃO: O FAST-RECOVERY CONGESTÃO check
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
            data, (ip, client_port) = self.connection.recvfrom(MSS + 270) #  + 268
            dicionario = build_dict(str(data, encoding="utf-8"))
            # salvando mensagem do servidor no log
            Log.ocorrido += f'\nO Cliente em {ip}:{client_port} enviou:\n'
            Log.ocorrido += f'Número de sequênica: {dicionario["seq_number"]}\t|\tSyn: {dicionario["syn"]}\t|\tTamaho do header: {dicionario["tam_header"]}\t|\tTamanho total: {dicionario["janela"]}\t|\tNúmero de confirmação: {dicionario["ack_number"]}\n'        
            Log.ocorrido += f'Dados: {dicionario["data"]}\n'        
            
            if dicionario["fin"] == "1":
                break
                        
            file.write(dicionario["data"])
            
            # seq_number
            if (self.seq == 0):
                self.seq = randint(0, 100)
            else:
                self.seq += self.len_res
            
            # ack_number
            if (self.ack == 0):
                self.ack = int(dicionario["seq_number"])
            else:
                if (int(self.seq) + int(self.len_res) == int(dicionario["ack_number"])): 
                    if self.buffer[0] != -1:
                        index = 0
                        while index < len(self.buffer):
                            if self.buffer[index] == -1:
                                break
                            self.ack += self.buffer[index]
                            self.buffer[index] = -1
                            index += 1
                    self.ack = int(dicionario["janela"]) + int(dicionario["seq_number"]) 
                else:
                    index = 0
                    while index < len(self.buffer):
                        if self.buffer[index] != -1:
                            index += 1
                        else:
                            break
                    self.buffer[index] = int(dicionario["janela"])
                
            
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
                                checksum=0)
            ack_buildado = ack.build()
            ack.tam_header = len(ack_buildado)
            self.connection.sendto(ack.build(), (ip, client_port))
            dicionario = build_dict(str(ack.build(), encoding="utf-8"))
            # salvando mensagem do servidor no log
            Log.ocorrido += f'\nO Servidor em {ip}:{client_port} enviou:\n'
            Log.ocorrido += f'Número de sequênica: {dicionario["seq_number"]}\t|\tSyn: {dicionario["syn"]}\t|\tTamaho do header: {dicionario["tam_header"]}\t|\tTamanho total: {dicionario["janela"]}\t|\tNúmero de confirmação: {dicionario["ack_number"]}\n'        
            Log.ocorrido += f'Dados: {dicionario["data"]}\n' 
        Log.escrever_log()
        sleep(3)
        self.connection.close()
        
if __name__ == '__main__':
    servidor = Server()
    servidor.start_server()






