from constCS import *

# SERVIDOR DO GERENCIADOR E ADMINISTRADOR
context = zmq.Context()
p = "tcp://"+ PREDIO_PRIVADO +":"+ PORT2 # how and where to connect
s  = context.socket(zmq.REP)    # servidor do gerenciador
s.bind(p)                      # bind socket to address

# CLIENTE DO ANDAR 1
pa1 = "tcp://"+ ANDAR_PRIVADO +":"+ PORT3 # ip e porta do andar 1
ca1 = context.socket(zmq.REQ)     # cliente do Andar 1
ca1.connect(pa1)                   # conectado no Andar 1

# CLIENTE DO ANDAR 2
pa2 = "tcp://"+ ANDAR2_PRIVADO +":"+ PORT3 # ip e porta do andar 2
ca2 = context.socket(zmq.REQ)     # cliente do Andar 2
ca2.connect(pa2)                   # conectado no Andar 2

# CLIENTE DO ANDAR 3
pa3 = "tcp://"+ ANDAR3_PRIVADO +":"+ PORT3 # ip e porta do andar 2
ca3 = context.socket(zmq.REQ)     # cliente do Andar 3
ca3.connect(pa3)                   # conectado no Andar 3

predio_MAX = 45 # 45
lista_espera_MAX = 15 # 15
predio_atual = "predio1"
identificador_predio = {1 : "predio 1", 2 : "Predio 2"} # identificadores do predio
frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista de ids
andar_socket = {"andar1" : ca1, "andar2" : ca2, "andar3" : ca3}
pessoasrem = "0 0 0"
# temporizador = 1

# lista de pesoas na espera
lista_atual = [] # lista de pessoas que estao no andar
lista_espera = [] # lista de pessoas na espera

# remove a(s) pessoa(s) do predio que o andar ja removeu
def funcao_remove(msg2):
  msg2 = msg2.split()
  # 0 = visitante, 1 = func cond, 2 = func empresa
  for i in range(3):
    if int(msg2[i]) > 0:
      for j in range(int(msg2[i])):
        if len(lista_atual) > 0:
          res = lista_atual.remove(frequentadores[i])
          print "\n- Saiu um " + frequentadores[i] + " do " + identificador_predio[1] + "\n"
          time.sleep(temporizador)
          print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) * Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"


def funcao_verifica_predio_adiciona_pessoa(pessoa, resposta):
  # verificando se a pessoa queria vir realmente para este predio
  if pessoa["predio"] == predio_atual:

    global pessoasrem

    # mandar a pessoa para o ANDAR 1
    andar_desejado = andar_socket[pessoa["andar"]]
    dic = {1 : "existe vaga?", "resposta" : str(resposta)}
    andar_desejado.send(str(dic)) # pergunta ao andar se existe vaga
    temp = ast.literal_eval(andar_desejado.recv()) # recebe resposta do andar 1 : se existe vaga e 2 : [lista de pessoas removidas]
    # print temp
    if temp[1] == "existe_vaga": # caso andar 1 ainda tenha vaga
      
      # dic = {1 : str(tipo)}
      dic = {1 : pessoa}
      andar_desejado.send(str(dic)) # envia dicionario com pessoa
      msg = ast.literal_eval(andar_desejado.recv()) # recebe resposta do andar {1 : status, 2 : qnt}
      # print msg
      
      if msg[1] == "ok": # pessoa entrou no andar
        lista_atual.append(pessoa["id"]) # adiciona uma pessoa no predio
        print "\n> Entrou um " + pessoa["id"] + " no " + identificador_predio[1] + "\n"
        print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) ** Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        
        # caso na resposta venha pessoa(s) para serem removidas do predio
        if msg[2] != "vazio": # existem pessoas que foram removidas, entao remova-as do predio
          funcao_remove(msg[2])
          pessoas_list = pessoasrem.split() # salva as pessoas a remover para enviar ao gerenciador na proxima oportunidades
          mensagem_list = msg[2].split()
          soma = ""
          for i in range(3):
              soma += "" + str(int(pessoas_list[i]) + int(mensagem_list[i])) + " "
          pessoasrem = soma
          # print str(pessoasrem) + "$"

        if resposta == "com": # apenas responde se houver pedido de resposta
          if pessoasrem != "0 0 0":
            del(msg[2])
            msg[2] = pessoasrem # msg[2] recebe o novo valor atualizado de pessoas a remover
            pessoasrem = "0 0 0" # zera o contador de pessoas a serem removidas antes de enviar
          # print msg
          s.send(str(msg)) # retorna um dic com [1] "ok"  e [2] qnt de pessoas a remover para o condominio, caso consiga adicionar a pessoa no predio e andar
      else:
        print "pessoa nao conseguiu entrar no andar\n" # nao pode acontecer
    
    elif temp[1] == "nao_existe_vaga":
      if len(lista_espera) < lista_espera_MAX: # caso ainda tenha vaga na lista de espera, adiciona a pessoa nela
        lista_espera.append(pessoa)
        print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) *** Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        dic = {1 : "ok"} # msg que identifica que pessoa foi adicionada na lista de espera com sucesso
        del(temp[1])
        dic.update(temp)

        # caso na resposta venha pessoa(s) para serem removidas do predio
        if temp[2] != "vazio": # existem pessoas que foram removidas, entao remova-as do predio
          funcao_remove(temp[2])
          pessoas_list = pessoasrem.split() # salva as pessoas a remover para enviar ao gerenciador na proxima oportunidades
          mensagem_list = temp[2].split()
          soma = ""
          for i in range(3):
              soma += "" + str(int(pessoas_list[i]) + int(mensagem_list[i])) + " "
          pessoasrem = soma
          # print str(pessoasrem) + "$$"

        if resposta == "com": # apenas responde se houver pedido de resposta
          if pessoasrem != "0 0 0":
            del(dic[2])
            dic[2] = pessoasrem # dic[2] recebe o novo valor atualizado de pessoas a remover
            pessoasrem = "0 0 0" # zera o contador de pessoas a serem removidas antes de enviar
          s.send(str(dic)) # retorna um dic com [1] "ok"  e [2] qnt de pessoas a remover para o condominio, caso consiga adicionar a pessoa no predio e andar
      elif len(lista_espera) >= lista_espera_MAX:
        print "\n*** Lista de espera do " + identificador_predio[1] + " esta cheia ***\n"
        resp = {1 : "listacheia", 2 : str(pessoasrem)}
        pessoasrem = "0 0 0" # zera o contador de pessoas a serem removidas antes de enviar
        s.send(str(resp))

    if pessoasrem == "0 0 0":
        # print "\nEstado Consistente\n"
        pass
  else:
      print "nao sou o predio correto\n" # nunca deve ocorrer
      resp = {1 : "erro", 2 : str(pessoasrem)}
      pessoasrem = "0 0 0" # zera o contador de pessoas a serem removidas antes de enviar
      s.send(str(resp))

while True:

  # print "\nCapacidade do "+ str(identificador_predio[2]) + " = " + str(predio_MAX)

  # dorme 1 segundo antes de continuar
  time.sleep(temporizador)

  # se houver pessoa(s) na lista de espera e o predio estiver vaga entao envia a pessoa
  if len(lista_espera) > 0 and len(lista_atual) < predio_MAX:
    pessoa = lista_espera.pop(0) # remove o primeiro da lista_espera
    dic = {1 : "existe vaga?"}
    andar_desejado = andar_socket[pessoa["andar"]]
    andar_desejado.send(str(dic))
    resp = ast.literal_eval(andar_desejado.recv())
    # print resp
    if resp[1] == "existe_vaga":
      funcao_verifica_predio_adiciona_pessoa(pessoa, "sem")
    elif resp[1] == "nao_existe_vaga":
      # caso na resposta venha pessoa(s) para serem removidas do predio
      if resp[2] != "vazio": # existem pessoas que foram removidas, entao remova-as do predio
        funcao_remove(resp[2])
        pessoas_list = pessoasrem.split() # salva as pessoas a remover para enviar ao gerenciador na proxima oportunidades
        mensagem_list = resp[2].split()
        soma = ""
        for i in range(3):
            soma += "" + str(int(pessoas_list[i]) + int(mensagem_list[i])) + " "
        pessoasrem = soma
        print str(pessoasrem) + "$$$"
      lista_espera.append(pessoa) # adiciona na lista de espera do predio
      if pessoasrem == "0 0 0":
        # print "\nEstado Consistente\n"
        pass
  
  # recebe uma nova pessoa do condominio
  pessoa = ast.literal_eval(s.recv())    # converte uma string em dicionario
  # print "\nMsg recebida: " + str(pessoa)

  # Setando configuracoes recebidas do ADM ou recebidas do gerenciador
  if bool(1 in pessoa):
    if(pessoa[1] == 0): # apenas envia a capacidade atual do predio
      s.send(str(predio_MAX))
      continue
    else:
      antes = predio_MAX
      predio_MAX = pessoa[1]
      print "\n*******************************"
      # print "| Nova capacidade do predio1 |
      # print "| Antes = 60                 |
      # print "| Agora = 10                 |
      print "| Nova capacidade do "+ str(identificador_predio[2]) + " |\n| Antes = " + str(antes) + "                  |\n| Agora = " + str(predio_MAX) + "                  |"
      print "*******************************\n"
      dic = {1 : "ok"}
      s.send(str(dic))
      continue
  elif bool(2 in pessoa):
    if(pessoa[2] == 0): # apenas envia a capacidade da fila de espera atual do predio
      s.send(str(lista_espera_MAX))
      continue
    else:
      antes = lista_espera_MAX
      lista_espera_MAX = pessoa[2]
      print "\n********************************************"
      # print "| Capacidade da fila de espera do predio1 |
      # print "| Antes = 60                              |
      # print "| Agora = 10                              |
      print "| Capacidade da fila de espera do "+ str(identificador_predio[2]) + " |\n| Antes = " + str(antes) + "                               |\n| Agora = " + str(lista_espera_MAX) + "                               |"
      print "********************************************\n"
      dic = {1 : "ok"}
      s.send(str(dic))
      continue
  elif bool(0 in pessoa):
    ca1.send(str(pessoa))
    resp1 = ca1.recv()
    ca2.send(str(pessoa))
    resp2 = ca2.recv()
    ca3.send(str(pessoa))
    resp3 = ca3.recv()
    if resp1 == "reiniciado" and resp2 == "reiniciado" and resp3 == "reiniciado":
      del lista_atual[:]
      del lista_espera[:]
      print "\n*******************************"
      print "| Reinicializado com sucesso! |"
      print "*******************************\n"
      s.send("reiniciado")
    else:
      print ("Erro ao reiniciar\n")
      s.send("nao_reiniciado")
    continue

  if len(lista_atual) < predio_MAX:  # caso ainda tenha vaga no andar e o tamanho da lista de espera seja menor que lista_espera_MAX
    # print "lista atual = " + str(len(lista_atual))
    # print "predio_MAX = " + str(predio_MAX)
    funcao_verifica_predio_adiciona_pessoa(pessoa, "com")
  elif len(lista_espera) < lista_espera_MAX: # caso ainda tenha vaga na lista de espera, adiciona a pessoa nela
    lista_espera.append(pessoa)
    print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) **** Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"

    resp = {1 : "ok", 2 : str(pessoasrem)}
    pessoasrem = "0 0 0" # zera o contador de pessoas a serem removidas antes de enviar
    s.send(str(resp)) # retorna "ok" para o condominio, caso consiga adicionar a pessoa no predio
  elif len(lista_espera) >= lista_espera_MAX:
    print "\n*** Lista de espera do " + identificador_predio[1] + " esta cheia ***\n"
    resp = {1 : "listacheia", 2 : str(pessoasrem)}
    # pessoasrem = "0 0 0" # zera o contador de pessoas a serem removidas antes de enviar
    s.send(str(resp))
    if len(lista_atual) > 0:
      # funcao_remove()   # chama a funcao remove
      pass
    continue