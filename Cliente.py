from socket import *


if __name__ == '__main__':
    host = 'localhost'
    port = 13000

    connection = socket(AF_INET, SOCK_DGRAM)
    
    numeros = []
    palavras = []
    for i in range(1, 21):
        numeros.append(i)
        if i % 2 == 0:
            palavras.append('a'*i)       
        else:
            palavras.append('b'*i)   
    print(numeros, palavras)     
    
    for i in range(len(numeros)):
        info = ""
        info += str(numeros[i])
        info += ' => '
        info += palavras[i]

        connection.sendto(bytes(info, encoding='utf8'), (host, port))
    
        msgServidor = connection.recvfrom(1024)
        print(str(msgServidor[0], 'utf-8'))

