from socket import *
from time import sleep
from Segmento import Segmento
from VariaveisControle import *
from Functions import *
import math
from random import randint, random


class Client:
    def __init__(self) -> None:
        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.response = None
        self.ip = None
        self.port = None
        self.buffer = None
        self.ack = 0
        self.len_res = 0
        self.seq = 0

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
            seg = segmento_inicial.build()
            segmento_inicial.tam_header = len(seg)
            self.connection.sendto(segmento_inicial.build(), (ip_destino, porta_destino))
            data, (ip, client_port) = self.connection.recvfrom(MSS)
            # salvando resposta do servidor no log
            dictServidor = build_dict(str(data, encoding="utf-8"))
                        
            if (dictServidor["syn"] == "1"):
                try:
                    self.buffer = [-1 for i in range(int(dictServidor["janela"]))]

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
                    seg2 = segmento_final.build()
                    segmento_final.tam_header = len(seg2)
                    self.connection.sendto(segmento_final.build(), (ip_destino, porta_destino))
                    print("Terminou o aperto de mão")
                except error:
                    print("Conexão perdida, tente novamente.")

        except error:
            print("Conexão perdida, tente novamente.")
    
    def enviar_dados(self, host, port):
        # dados = "Key Point: If the environment variable GOOGLE_ADS_CONFIGURATION_FILE_PATH is set when the load_from_env method is called, then configuration values will be retrieved from the google-ads.yaml file located at the specified path, not from the environment variables described above.\nComo prática recomendada, o ideal é configurar a API para usar o roteamento de caminho com diferenciação de maiúsculas e minúsculas. Assim, a API retorna um código de status HTTP 404 quando o método solicitado na URL não corresponde ao nome do método de API listado na especificação OpenAPI. Os frameworks de aplicativos da Web, como o Node.js Express, têm uma configuração para ativar ou desativar o roteamento com diferenciação de maiúsculas e minúsculas. O comportamento padrão depende da biblioteca utilizada. Convém rever as configurações na biblioteca para ter certeza de que o roteamento com diferenciação de maiúsculas e minúsculas está ativado. Essa recomendação coincide com o v2.0 da especificação OpenAPI, que afirma: Todos os nomes de campo na especificação diferenciam maiúsculas de minúsculas"
        file = open("./shrek.txt", "r")
        dados = file.read()
        # print(tamanhoDados)
        # ALTERAR DPS
        self.seq = randint(0, 100)
        cabecalho = Segmento(host_origem=host,
                            port_origem=port,
                            host_destino=host,
                            port_destino=port,
                            flags=1,
                            syn=0,
                            fin=0,
                            seq_number=-1,
                            ack_number=0,
                            ack_flag=1,
                            tam_header=0,
                            janela=janelaAtual,    # tem que atualizar esse janela atual, dizendo quantos segmentos ainda podem ser enviados
                            checksum=0)
        tamanhoCabecalho = len(cabecalho.build()) 
        cabecalho.data = dados
        cabecalho.tam_header = tamanhoCabecalho
        tamanhoDados = len(cabecalho.build()) 

        if(tamanhoDados > MSS):
            quantidadeDeSegmentos = math.ceil(tamanhoDados/MSS)
            # quantidadeDeSegmentos = math.ceil((tamanhoDados - 270)/(MSS - 270))
            
            segmentos = []
            for i in range(quantidadeDeSegmentos):
                if i == 0: 
                    new_dados = dados[: MSS]     
                    # new_dados = dados[: math.ceil((MSS - 270))] 
                else:
                    new_dados = dados[i*MSS : (i+1)*MSS] 
                    # new_dados = dados[math.ceil(i*(MSS - 270)) : math.ceil((i+1)*(MSS - 270))] 
                
                cabecalho.set_data(new_dados)
                new_cabecalho = cabecalho.clone()
                segmentos.append(new_cabecalho) 
            
            cwnd_local = 1
            acks_duplicados = 0
            # ssthresh = math.inf
            ssthresh = 8
            passou_ss = False
            rec_rap = False
            while len(segmentos) != 0:
                fila = []
                enviados = 0
                for i in range(cwnd_local):
                    try:
                        fila.append(segmentos.pop(0))
                        enviados += 1
                    except:
                        break
                
                aux_seq_number = self.seq
                for i in range(enviados):
                    segmento = fila[i]

                    self.len_res = len(fila[i].data)
                    segmento.ack_number = self.ack

                    if segmento.seq_number == -1:
                        aux_seq_number = self.seq + self.len_res  
                        segmento.seq_number = aux_seq_number
                        self.seq = segmento.seq_number

                    segmento.janela = self.len_res                    
                    self.connection.sendto(segmento.build(), (host, port))
                
                index = 0
                recebeu = False
                # ack_repetido = False
                if not passou_ss and not rec_rap:
                    # slow start
                    print("slow start")
                    for i in range(enviados):
                        index = i
                        data, (ip, client_port) = self.connection.recvfrom(MSS)
                        dicionario = build_dict(str(data, encoding="utf-8"))
                        # salvando resposta do servidor no log
                        
                        recebeu = True
                        
                        if (self.ack == 0):
                            self.ack = int(dicionario["seq_number"])
                        else:
                            if (fila[i].seq_number + fila[i].janela == int(dicionario["ack_number"])):   
                                self.ack = int(dicionario["seq_number"]) + int(dicionario["janela"])
                                cwnd_local += 1
                                acks_duplicados = 0
                                if cwnd_local >= ssthresh:
                                    passou_ss = True
                                    break
                            else:
                                acks_duplicados += 1
                                segmentos.insert(0, fila[i])
                                if acks_duplicados == 3:
                                    ssthresh = cwnd_local // 2
                                    cwnd_local = ssthresh + 3
                                    rec_rap = True
                            
                if passou_ss:
                    # prevenção de congestionamento, começando do index
                    print("prevenção de congestionamento")
                    for i in range(index, enviados):
                        if not recebeu:
                            data, (ip, client_port) = self.connection.recvfrom(MSS)
                            dicionario = build_dict(str(data, encoding="utf-8"))
                            # salvando resposta do servidor no log
                        
                        if (self.ack == 0):
                            self.ack = int(dicionario["seq_number"])
                        else:
                            if (fila[i].seq_number + fila[i].janela == int(dicionario["ack_number"])):   
                                self.ack = int(dicionario["seq_number"]) + int(dicionario["janela"])
                                cwnd_local += round(cwnd_local*1/cwnd_local)  # verificar se está correto
                                acks_duplicados = 0
                            else:
                                acks_duplicados += 1
                                segmentos.insert(0, fila[i])
                                if acks_duplicados == 3:
                                    ssthresh = cwnd_local // 2
                                    cwnd_local = ssthresh + 3
                                    rec_rap = True
                                    passou_ss = False

                # recuperação rápida
                if rec_rap:
                    print("recuperação rápida")
                    for i in range(enviados):
                        index = i
                        if not recebeu:
                            data, (ip, client_port) = self.connection.recvfrom(MSS)
                            dicionario = build_dict(str(data, encoding="utf-8"))
                            # salvando resposta do servidor no log

                        if (self.ack == 0):
                            self.ack = int(dicionario["seq_number"])
                        else:
                            if (fila[i].seq_number + fila[i].janela == int(dicionario["ack_number"])):   
                                self.ack = int(dicionario["seq_number"]) + int(dicionario["janela"])
                                cwnd_local = ssthresh
                                acks_duplicados = 0
                                rec_rap = False
                                passou_ss = True
                            else:
                                segmentos.insert(0, fila[i])
                                cwnd_local += 1
        else:
            self.connection.sendto(cabecalho.build(), (host, port))
        
        self.terminar_conexao()
                
    def terminar_conexao(self):
        cabecalho = Segmento(host_origem=host,
                                    port_origem=port,
                                    host_destino=host,
                                    port_destino=port,
                                    flags=1,
                                    syn=0,
                                    fin=1,
                                    seq_number=self.seq,
                                    ack_number=0,
                                    ack_flag=0,
                                    tam_header=tamanhoHeader,
                                    janela=janelaAtual,
                                    checksum=0)
        self.connection.sendto(cabecalho.build(), (host, port))
        self.connection.close() 
        print("Finalizando conexão")
        

if __name__ == '__main__':
    cliente1 = Client()
    cliente1.criar_conexao(host, port)
    cliente1.enviar_dados(host, port)
            
            

