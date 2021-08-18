from socket import *
from VariaveisControle import *


def start_server():
    connection = socket(AF_INET, SOCK_DGRAM)
    connection.bind(('', port))
    print("Servidor de pé e ouvindo")

    # ouvindo possíveis datagramas que podem chegar
    while(True):
        data, (ip, client_port) = connection.recvfrom(1024)
        print(data)
        text = str(data, 'utf-8')
        # print("O Cliente em {}:{} enviou {}".format(ip, client_port, text))
        
        # enviando uma resposta para o cliente
        # msg = "OK - enviou " + str(data, 'utf-8')
        # connection.sendto(bytes(msg, encoding='utf8'), (ip, client_port))
        
if __name__ == '__main__':
    start_server()






