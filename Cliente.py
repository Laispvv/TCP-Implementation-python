from socket import *
from time import sleep
from Segmento import Segmento
from VariaveisControle import *


if __name__ == '__main__':
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
            
            

