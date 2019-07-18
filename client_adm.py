from constCS import *

# CLIENTE DO PREDIO 1
context = zmq.Context()
p = "tcp://"+ PREDIO_PUBLICO +":"+ PORT2 # how and where to connect
s  = context.socket(zmq.REQ)    # cria socket de requisicao
s.connect(p)                   # block until connected

# CLIENTE DO PREDIO 2
context = zmq.Context()
p2 = "tcp://"+ PREDIO2_PUBLICO +":"+ PORT2 # how and where to connect
s2  = context.socket(zmq.REQ)    # cria socket de requisicao
s2.connect(p2)                   # block until connected

predios = {1 : "predio1", 2 : "predio2"} #, 3 : "predio3", 4 : "predio4"}
predio_socket = {"predio1" : s, "predio2" : s2} #, "predio3" : s3, "predio4" : s4}

controle, lista_atual_qnt, lista_espera_qnt = 1, 0, 0
capacidade_atual = {1 : 0, 2 : 0} # capacidades atuais dos predios
tamanho_atual = {1 : 0, 2 : 0} # capacidades atuais das filas de espera dos predios

# recebendo as capacidades dos predios antes de executar o script
for i in range(1,3):
    for j in range(1,3):
        dic = {j : 0}
        predio_socket[predios[i]].send(str(dic))
        resposta = ast.literal_eval(predio_socket[predios[i]].recv())
        # print resposta
        if j == 1:
            capacidade_atual[i] = resposta
        elif j == 2:
            tamanho_atual[i] = resposta

while controle != 0:

    op = input ("\n** BEM VINDO - MODULO ADMINISTRADOR **\n\n\t[1] - Alterar a capacidade maxima de um Predio\n\t      Predio1[{}]\tPredio2[{}]\n\t[2] - Alterar o tamanho da lista de espera de um Predio\n\t      Predio1[{}]\tPredio2[{}]\n\t[0] - SAIR\n>: ".format(capacidade_atual[1], capacidade_atual[2], tamanho_atual[1], tamanho_atual[2]))
    if op == 1: # alterar capacidade maximo do predio 1
        predio_desejado = 0
        while predio_desejado not in [1, 2]:
            predio_desejado = input ("\nInforme qual o PREDIO desejado? [1 , 2]\n>: ")
        
        nova_capacidade = input ("\nInforme a nova capacidade [ATUAL: {}]\n:> ".format(capacidade_atual[predio_desejado]))
        capacidade_atual[predio_desejado] = nova_capacidade
        dic = {1 : nova_capacidade}
        predio_socket[predios[predio_desejado]].send(str(dic))
        resposta = ast.literal_eval(predio_socket[predios[predio_desejado]].recv())
        if resposta[1] == "ok":
            print "\n************************************"
            # print "| Nova capacidade do predio1 = 10 |"
            print "| Nova capacidade do predio " + str(predio_desejado) + " = " + str(nova_capacidade) + " |"
            print "************************************\n"
            time.sleep(2)
        else:
            print "\nErro ao aplicar nova capacidade maxima do predio \n" + str(predio_desejado) + "!\n"
            time.sleep(2)

    elif op == 2:
        predio_desejado = 0
        while predio_desejado not in [1, 2]:
            predio_desejado = input ("\nInforme qual o PREDIO desejado? [1 , 2]\n>: ")
                
        novo_tamanho = input ("\nInforme o novo tamanho da lista de espera [ATUAL: {}]\n:> ".format(tamanho_atual[predio_desejado]))
        tamanho_atual[predio_desejado] = novo_tamanho
        dic = {2 : novo_tamanho}
        predio_socket[predios[predio_desejado]].send(str(dic))
        resposta = ast.literal_eval(predio_socket[predios[predio_desejado]].recv())
        if resposta[1] == "ok":
            print "\n*******************************************************"
            # print "| Nova capacidade da lista de espera do predio 1 = 10 |"
            print "| Nova capacidade da lista de espera do predio " + str(predio_desejado) + " = " + str(novo_tamanho) + " |"
            print "*******************************************************\n"
            time.sleep(2)
        else:
            print "\nErro ao aplicar nova capacidade maxima da lista do predio \n" + str(predio_desejado) + "!\n"
            time.sleep(2)

    elif op == 0: # sair
        controle = 0
        
    else:
        print "\nComando invalido, tente novamente!\n"