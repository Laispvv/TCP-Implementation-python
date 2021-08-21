from socket import *
from time import sleep
from Segmento import Segmento
from VariaveisControle import *
from Functions import *
import math


class Client:
    def __init__(self) -> None:
        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.response = None
        self.ip = None
        self.port = None

    def criar_conexao(self, ip_destino, porta_destino):
        try:
            segmento_inicial = Segmento(host_origem=host,
                                        port_origem=port,
                                        host_destino=host,
                                        port_destino=port,
                                        flags=0,
                                        syn=1,
                                        fin=0,
                                        seq_number=numeroSequencia,
                                        ack_number=0,
                                        ack_flag=0,
                                        tam_header=tamanhoHeader,
                                        janela=janelaAtual,
                                        checksum=0)
            self.connection.sendto(segmento_inicial.build(), (ip_destino, porta_destino))
            msgServidor = str(self.connection.recvfrom(MSS)[0], encoding="utf-8") 
            # listServidor = msgServidor.split(",")
            # listServidor = map(lambda x : x.split(":"), listServidor)
            dictServidor = build_dict(msgServidor)
            if (dictServidor["syn"] == "1"):
                try:
                    buffer = [0 for i in range(int(dictServidor["janela"]))]

                    segmento_final = Segmento(host_origem=host,
                                        port_origem=port,
                                        host_destino=host,
                                        port_destino=port,
                                        flags=0,
                                        syn=0,
                                        fin=0,
                                        seq_number=numeroSequencia,
                                        ack_number=int(dictServidor["seq_number"])+1,
                                        ack_flag=1,
                                        tam_header=tamanhoHeader,
                                        janela=janelaAtual,
                                        checksum=0) 
                    self.connection.sendto(segmento_final.build(), (ip_destino, porta_destino))
                    print("Terminou o aperto de mão")
                except error:
                    print("Conexão perdida, tente novamente.")

        except error:
            print("Conexão perdida, tente novamente.")
    
    def enviar_dados(self, host, port):
        dados = "Key Point: If the environment variable GOOGLE_ADS_CONFIGURATION_FILE_PATH is set when the load_from_env method is called, then configuration values will be retrieved from the google-ads.yaml file located at the specified path, not from the environment variables described above.\nComo prática recomendada, o ideal é configurar a API para usar o roteamento de caminho com diferenciação de maiúsculas e minúsculas. Assim, a API retorna um código de status HTTP 404 quando o método solicitado na URL não corresponde ao nome do método de API listado na especificação OpenAPI. Os frameworks de aplicativos da Web, como o Node.js Express, têm uma configuração para ativar ou desativar o roteamento com diferenciação de maiúsculas e minúsculas. O comportamento padrão depende da biblioteca utilizada. Convém rever as configurações na biblioteca para ter certeza de que o roteamento com diferenciação de maiúsculas e minúsculas está ativado. Essa recomendação coincide com o v2.0 da especificação OpenAPI, que afirma: Todos os nomes de campo na especificação diferenciam maiúsculas de minúsculas"
        dados2 = dados[:1050]
        # print(tamanhoDados)
        # ALTERAR DPS
        cabecalho = Segmento(host_origem=host,
                                    port_origem=port,
                                    host_destino=host,
                                    port_destino=port,
                                    flags=1,
                                    syn=0,
                                    fin=0,
                                    seq_number=numeroSequencia,
                                    ack_number=numeroSequencia+1,
                                    ack_flag=1,
                                    tam_header=tamanhoHeader,
                                    janela=janelaAtual,
                                    checksum=0)
        tamCabecalho = len(cabecalho.build())
        # print(len(cabecalho.build()))
        cabecalho.data = bytes(dados, encoding='utf-8')
        tamanhoDados = len(cabecalho.build())
        # print(tamanhoDados)
        # print(len(dados))
        
        if(tamanhoDados > MSS-tamCabecalho):
            # print(tamanhoDados)
            # quantidadeDeSegmentos = math.ceil(tamanhoDados/MSS)
            quantidadeDeSegmentos = tamanhoDados//MSS
            sobras = tamanhoDados % MSS
            
            #enviando os dados de tamanho inteiro
            segmentos = []
            for i in range(quantidadeDeSegmentos):
                if i == 0:
                    new_dados = dados[: math.ceil((MSS/1.3) - tamCabecalho)]
                else:
                    new_dados = dados[i*MSS - tamCabecalho : (i+1)*MSS - tamCabecalho]   # provavelmente tenho que arrumar
                
                # dados_enviar = bytes(new_dados, encoding='utf-8')
                # cabecalho.set_data(dados_enviar)
                # print(new_dados)
                # print()
                cabecalho.set_data(new_dados)
                new_cabecalho = cabecalho.clone()
                segmentos.append(new_cabecalho) 

            if sobras != 0 :
                if quantidadeDeSegmentos == 1:
                    new_dados = dados[math.ceil((MSS/1.3) - tamCabecalho):]
                else:
                    # cabecalho.data=bytes(dados[(quantidadeDeSegmentos-1)*MSS - tamCabecalho:], encoding='utf-8')       
                    new_dados = dados[(quantidadeDeSegmentos-1)*MSS - tamCabecalho:]     # provavelmente tenho que arrumar
                # print(new_dados)
                cabecalho.set_data(new_dados)
                new_cabecalho = cabecalho.clone()
                segmentos.append(new_cabecalho) 

            for segmento in segmentos:
                # print(segmento.data)
                # print()
                self.connection.sendto(segmento.build(), (host, port))
            self.terminar_conexao()
        else:
            # print(len(cabecalho.build()))
            self.connection.sendto(cabecalho.build(), (host, port))
                
    def terminar_conexao(self):
        self.connection.close() 
        print("Finalizando conexão")
        

if __name__ == '__main__':
    cliente1 = Client()
    cliente1.criar_conexao(host, port)
    cliente1.enviar_dados(host, port)
    # cliente1.terminar_conexao()

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
            
            

