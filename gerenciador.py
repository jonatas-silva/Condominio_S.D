from constCS import *

# SERVIDOR DO CLIENTE APP
context = zmq.Context()
p = "tcp://"+ GERENCIADOR_PRIVADO +":"+ PORT1
s  = context.socket(zmq.REP)
s.bind(p)

# CLIENTE DO PREDIO 1
p2 = "tcp://"+ PREDIO_PRIVADO +":"+ PORT2
s2  = context.socket(zmq.REQ)
s2.connect(p2)

# CLIENTE DO PREDIO 2
p3 = "tcp://"+ PREDIO2_PUBLICO +":"+ PORT2
s3  = context.socket(zmq.REQ)
s3.connect(p3)

condominio_MAX = 240 # 240 capacidade maxima dentro condominio [desconsiderando a lista de espera]
lista_espera_MAX = 30 # 10

frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista
predio_socket = {"predio1" : s2, "predio2" : s3} # , "predio3" : s4, "predio4" : s5} # dicionario que vincula um predio ao seu socket
# temporizador = 1

# lista de pesoas na espera
lista_atual = [] # lista de pessoas que estao no condominio
lista_espera = [] # lista de pessoas na espera

# remove a(s) pessoa(s) do condominio que o andar ja removeu
def funcao_remove(pessoa, msg2):
  msg2 = msg2.split()
  # 0 = visitante, 1 = func cond, 2 = func empresa
  for i in range(3):
    if int(msg2[i]) > 0:
      for j in range(int(msg2[i])):
        if len(lista_atual) > 0:
          res = lista_atual.remove(frequentadores[i])
          print "\n- Saiu um " + frequentadores[i] + " do condominio : " + pessoa["predio"] + " : " + pessoa["andar"] + "\n"
          time.sleep(temporizador)
          print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) * Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"

# analisa a msg do predio [andar] sobre a pessoa
def resposta_predio(pessoa, msg):

    # caso na resposta venha pessoa(s) para serem removidas do predio
    if msg[2] != "vazio" and msg[2] != "0 0 0": # existem pessoas que foram removidas, entao remova-as do predio
        funcao_remove(pessoa, msg[2])

    if msg[1] == 'ok':
        lista_atual.append(pessoa["id"]) # adiciona uma pessoa no condominio
        print "\n> Entrou um " + pessoa["id"] + " no condominio : " + pessoa["predio"] + " : " + pessoa["andar"] + "\n"
        print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) ** Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        
        # informacoes sobre o condominio [gerenciador] enviadas para o cliente
        dic = {1 : len(lista_atual), 2 : len(lista_espera), 3 : msg[2]}
        s.send(str(dic))
    elif msg[1] == "erro":
        print "O " + pessoa["id"] + " nao possui acesso ao predio interessado!\n"
    elif msg[1] == "listacheia":
        if len(lista_espera) < lista_espera_MAX:
            lista_espera.append(pessoa)
            print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) *** Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        else:
            print "\n O condominio esta cheio no momento, volte mais tarde!\n"
    else:
        print "erro_app\n"

# verificar se nao existe pessoas na lista de espera do condominio
def verifica_pessoas_fila_espera():
  if len(lista_espera) > 0 and len(lista_atual) < condominio_MAX:
    temp = lista_espera.pop(0) # remove o primeiro da lista_espera
    
    predio_destino = predio_socket[temp["predio"]]
    predio_destino.send(str(temp))
    msg = ast.literal_eval(predio_destino.recv())
    resposta_predio(pessoa, msg)


controle = 1
while controle != 0:

    # manda a pessoa recebida do cliente para o predio correto
    pessoa = ast.literal_eval(s.recv())
    # print pessoa

    # Caso receba um comando do Cliente
    if bool(0 in pessoa):
        i = 0
        for socket in predio_socket:
            predio_socket[socket].send(str(pessoa))
            resposta = predio_socket[socket].recv()
            i += 1
        
        if i == 2:
            del lista_atual[:]
            del lista_espera[:]
            print "\n*******************************"
            print "| Reinicializado com sucesso! |"
            print "*******************************\n"
            s.send("reiniciado")
            continue
        else:
            print ("Erro ao reiniciar\n")
            s.send("nao_reiniciado")
            continue

    if len(lista_atual) < condominio_MAX:

        # verifica se nao existe pessoas na lista de espera do condominio
        while len(lista_espera) > 0 and len(lista_atual) < condominio_MAX:
            verifica_pessoas_fila_espera()

        # envia a pessoa para o predio desejado
        print pessoa
        predio_destino = predio_socket[pessoa["predio"]]
        predio_destino.send(str(pessoa))
        msg = ast.literal_eval(predio_destino.recv())
        # print msg

        resposta_predio(pessoa, msg)
    elif len(lista_espera) < lista_espera_MAX:
        lista_espera.append(pessoa)
        print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) ***** Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        
        # informacoes sobre o condominio [gerenciador] enviadas para o cliente
        dic = {1 : len(lista_atual), 2 : len(lista_espera)}
        s.send(str(dic))
    elif len(lista_espera) >= lista_espera_MAX:
        print "\n*** Fila do condominio esta cheia ***\n"
        
        # informacoes sobre o condominio [gerenciador] enviadas para o cliente
        dic = {1 : len(lista_atual), 2 : len(lista_espera)}
        s.send(str(dic))