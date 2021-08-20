from socket import *
from time import sleep
from Segmento import Segmento
from VariaveisControle import *
from Functions import *


class Client:
    def __init__(self) -> None:
        self.connection = None
        self.response = None
        self.ip = None
        self.port = None

    def criar_conexao(self, ip_destino, porta_destino):
        try:
            self.connection = socket(AF_INET, SOCK_DGRAM)
            segmento_inicial = Segmento() # colocar os dados
            self.connection.sendto(segmento_inicial.build(), (ip_destino, porta_destino))
            msgServidor = str(self.connection.recvfrom(MSS)[0], encoding="utf-8") 
            listServidor = msgServidor.split(",")
            listServidor = map(lambda x : x.split(":"), listServidor)
            dictServidor = build_dict(list(listServidor))
            if (dictServidor["SYN"] == "1"):
                try:
                    # alocar varíaveis que vieram do servidor

                    segmento_final = Segmento()  # colocar os dados
                    self.connection.sendto(segmento_final.build(), (ip_destino, porta_destino))
                except error:
                    print("Conexão perdida, tente novamente.")

        except error:
            print("Conexão perdida, tente novamente.")
    
    def terminar_conexao(self):
        print("Finalizando conexão")

if __name__ == '__main__':
    cliente1 = Client()
    cliente1.criar_conexao(host, port)

    """"
    connection = socket(AF_INET, SOCK_DGRAM)
    estaConectado = True
    
    numeros = []
    palavras = []
    for i in range(1, 200):
        numeros.append(i)
        if i % 2 == 0:
            palavras.append('a')       
        else:
            palavras.append('b')   
    
    # enviando dados para o servidor    
    for i in range(len(numeros)):
        info = ""
        info += str(numeros[i])
        info += ' => '
        info += palavras[i]
        try:
            segmento = Segmento(host, port, host, port, 0b000, 0, 0, 0, tamanhoHeader, 0, 0, info)
            # s = socket(AF_INET, SOCK_RAW, SOCK_DGRAM)
            connection.sendto(segmento.build(), (host, port))
            msgServidor = connection.recvfrom(1024)
            print(msgServidor)
        except error:
            estaConectado = False
            connection = socket()
            print("Conexão perdida... reconectando.")
            while not estaConectado:
                try:
                    connection.connect((host, port))
                    estaConectado = True
                    print("Reconectado com sucesso.")
                except error:
                    sleep(2)
    connection.close() 
    """
            
            

