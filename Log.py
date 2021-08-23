ocorrido = ''

def escrever_log():
    log = open("log.txt", "w")
    print("chegou aqui")
    log.write(ocorrido)
    log.close()
    print("chegou aqui")
