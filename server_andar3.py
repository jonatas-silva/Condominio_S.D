from constCS import *

# SERVIDOR DO PREDIO
context = zmq.Context()
# p = "tcp://"+ HOST +":"+ PORT7 # how and where to connect
p = "tcp://"+ ANDAR3_PRIVADO +":"+ PORT3 # how and where to connect
s  = context.socket(zmq.REP)    # create reply socket
s.bind(p)                      # bind socket to address

andar1_MAX = 15 # 15 quantidade maximo de pessoas dentro do andar
identificador_andar = {1 : "andar 3", 2 : "Andar 3", 3 : "andar3"} # identificadores do andar
frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista
# temporizador = 1

lista_atual = [] # lista de pessoas que estao no andar

# remove alguma(s) pessoa(s) do andar (aleatoriamente)
def funcao_remove():  
  v1, v2, v3 = 0, 0, 0 # v1 = qnt visitante, v2 = qnt func cond, v3 = qnt func empresa
  for i in range(randint(1, 1)):
    if len(lista_atual) > 0:
      temp = lista_atual.pop(0)
      if (temp == frequentadores[0]):
        v1 += 1
      elif (temp == frequentadores[1]):
        v2 += 1
      elif (temp == frequentadores[2]):
        v3 += 1
      print "\n- Saiu um " + temp + " do " + identificador_andar[1] + "\n"
      time.sleep(temporizador)
      print identificador_andar[2] + " : [" + str(len(lista_atual)) + "] pessoa(s)\n"
  string = "{2 : \'" + str(v1) + " " + str(v2) + " "  + str(v3) + "\'}"
  return string

i = 0
while True:

  if len(lista_atual) > andar1_MAX:
    print "O " + identificador_andar[1] +" esta cheio!\n"
  
  message = ast.literal_eval(s.recv()) # recebe uma nova mensagem do predio
  # print str(i) + " --- " + str(message)

  # setando configuracoes recebidas
  if bool(0 in message):
    del lista_atual[:]
    print "\n*******************************"
    print "| Reinicializado com sucesso! |"
    print "*******************************\n"
    s.send("reiniciado")
    continue
  
  dic2 = {2 : "vazio"} # dicionario [vazio] indica que nao tem pessoas a remover

  # caso a messagem seja "existe vaga?" e tenha vaga no andar
  if message[1] == "existe vaga?" and len(lista_atual) < andar1_MAX:
    dic = {1 : "existe_vaga"}
    # print "oi"
    s.send(str(dic)) # retorna um dic com [1] "existe_vaga", dizendo que existe vaga no andar
    continue
  elif message[1] == "existe vaga?" and len(lista_atual) >= andar1_MAX:
    dic = {1 : "nao_existe_vaga"}

    # caso tenha mais que 5 pessoas no andar e a msg nao for "existe vaga?", chama a funcao (aleatoriamente) e remove algumas pessoas
    if len(lista_atual) > 5 and bool(getrandbits(1)) == True:
      dic2 = ast.literal_eval(funcao_remove()) # chama a funcao remove e converte a string retornada em dicionario

    dic.update(dic2) # concatena dic com dic2
    s.send(str(dic)) # retorna um dic com [1] "nao_existe_vaga" e [2] qnt de pessoas a remover para o predio, dizendo que nao existe vaga no andar
    continue

  # caso ainda tenha vaga no andar
  if len(lista_atual) < andar1_MAX:

    # verificando se a pessoa queria vir realmente para este andar
    if message[1]["andar"] == identificador_andar[3]:
      
      lista_atual.append(message[1]["id"]) # guarda na lista a identificacao da pessoa que esta entrando no andar
      print "\n> Entrou um " + message[1]["id"] + " no " + identificador_andar[1] + "\n"
      time.sleep(temporizador * 0.75)
      print identificador_andar[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) *\n"
      dic = {1 : "ok"} # msg que identifica que pessoa foi adicionada com sucesso

      # caso tenha mais que 5 pessoas no andar e a msg nao for "existe vaga?", chama a funcao (aleatoriamente) e remove algumas pessoas
      if len(lista_atual) > 5 and bool(getrandbits(1)) == True:
        dic2 = ast.literal_eval(funcao_remove()) # chama a funcao remove e converte a string retornada em dicionario

      dic.update(dic2) # concatena dic com dic2
      s.send(str(dic)) # retorna um dic com [1] "ok" e [2] qnt de pessoas a remover para o predio, caso consiga adicionar a pessoa no andar
    else:
      print "nao sou o andar correto\n" # nunca deve ocorrer
      continue
  else:
    print "O " + identificador_andar[2] + " esta cheio, aguarde no predio!\n"