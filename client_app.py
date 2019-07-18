from constCS import *

context = zmq.Context()
p = "tcp://"+ GERENCIADOR_PUBLICO +":"+ PORT1 # ip publico AWS
s  = context.socket(zmq.REQ)    # cria socket de requisicao
s.connect(p)                   # block until connected

frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista
frequentadores_dic = {1 : "visitante", 2 : "funcionario do condominio", 3 : "funcionario de empresa"} # dicionario
predios = {1 : "predio1", 2 : "predio2"} #, 3 : "predio3", 4 : "predio4"}
andares = {1 : "andar1", 2 : "andar2", 3 : "andar3"}

# controle de acesso
# def controle_acesso(id):
#     if id == "visitante":
#         acesso = [randint(1,4)]
#     elif id == "funcionario do condominio":
#         acesso = [1, 2, 3, 4]
#     else:
#         acesso = [randint(1,4), randint(1,4)]
#         while acesso[0] == acesso[1]:
#             acesso = [randint(1,4), randint(1,4)]
#     return acesso

controle, lista_atual_qnt, lista_espera_qnt = 1, 0, 0
qnt_predio1, qnt_predio2 = 0, 0
while controle != 0:

    op = input ("\n** BEM VINDO AO SIMULADOR DE CONDOMINIO DE EMPRESAS **\n\n\t[1] - Entrada automatizada\n\t[2] - Inserir uma pessoa manualmente\n\t[3] - Qnt TOTAL de pessoas no Condominio = [{}]\n\t      Predio1 [{}]\tPredio2 [ {} ]\n\t[4] - Qnt de pessoas dentro do Condominio = [{}]\n\t[5] - Qnt de pessoas na lista de espera do Condominio = [{}]\n\t[9] - Reiniciar aplicacao\n\t[0] - SAIR\n>: ".format(lista_atual_qnt+lista_espera_qnt, qnt_predio1, qnt_predio2, lista_atual_qnt, lista_espera_qnt))
    if op == 1: # teste automatizado
        casos_teste = input ("\nInforme a quantidade de instancias de pessoas (aleatorias) de entrada\n>: ")
        predio_destino = predios[input ("\npredio -> [1] - predio1\t[2] - predio2\n>: ")]
        andar_destino = andares[input ("\nandar -> [1] - andar1\t[2] - andar2\t[3] - andar3\n>: ")]
        for i in range(casos_teste):
            id = choice(frequentadores) # definindo (aleatoriamente) um tipo de pessoa
            # acesso = controle_acesso(id) # controle de acesso

            # exemplo de um tipo de Pessoa
            pessoa = {"id" : str(id), "predio" : str(predio_destino), "andar" : str(andar_destino), "acesso" : "###"}
            # print str(pessoa)

            s.send(str(pessoa)) # manda a pessoa para o gerenciador
            msg = ast.literal_eval(s.recv())

            if predio_destino == "predio1":
                qnt_predio1 += 1
            elif predio_destino == "predio2":
                qnt_predio2 += 1

            # print msg
            lista_atual_qnt = (msg[1] + msg[2])
            lista_espera_qnt = msg[2]

            print "\n*********************************************************************"
            print "\n> Entrou um " + pessoa["id"] + " no condominio : " + pessoa["predio"] + " : " + pessoa["andar"] + "\n\n"
            print "Condominio : [" + str(lista_atual_qnt) + "] pessoa(s) ** Lista de espera : [" + str(lista_espera_qnt) + "] pessoa(s)"
            print "\n*********************************************************************"

            time.sleep(1)

    elif op == 2: # inserir uma pessoa manualmente
        id = frequentadores_dic[input ("\nId -> [1] - visitante\t[2] - funcionario do condominio\t[3] - funcionario de empresa\n>: ")]
        predio_destino = predios[input ("\npredio -> [1] - predio1\t[2] - predio2\n>: ")]
        andar_destino = andares[input ("\nandar -> [1] - andar1\t[2] - andar2\t[3] - andar3\n>: ")]
        # acesso = input("politica de acesso -> 1 - visitante\t2 - fucionario do condominio\t3 - funcionario de empresa\n>: ")

        # exemplo de uma instancia de Pessoa
        pessoa = {"id" : str(id), "predio" : str(predio_destino), "andar" : str(andar_destino), "acesso" : str(id)}
        
        s.send(str(pessoa)) # manda a pessoa para o gerenciador
        msg = ast.literal_eval(s.recv())

        if predio_destino == "predio1":
            qnt_predio1 += 1
        elif predio_destino == "predio2":
            qnt_predio2 += 1

        # print msg
        lista_atual_qnt = (msg[1] + msg[2])
        lista_espera_qnt = msg[2]

        print "\n*********************************************************************"
        print "\n> Entrou um " + pessoa["id"] + " no condominio : " + pessoa["predio"] + " : " + pessoa["andar"] + "\n\n"
        print "Condominio : [" + str(lista_atual_qnt) + "] pessoa(s) ** Lista de espera : [" + str(lista_espera_qnt) + "] pessoa(s)"
        print "\n*********************************************************************"

        # caso na resposta venha pessoa(s) que foram removidas do predio
        if msg[3] != "vazio" and msg[3] != "0 0 0": # existem pessoas que foram removidas, entao imprima-as
            msg2 = msg[3].split()
            # 0 = visitante, 1 = func cond, 2 = func empresa
            for i in range(3):
                if int(msg2[i]) > 0:
                    for j in range(int(msg2[i])):
                        # if len(lista_atual) > 0:
                            print "\n- Saiu um " + frequentadores[i] + " do condominio : " + pessoa["predio"] + " : " + pessoa["andar"] + "\n"
                            time.sleep(temporizador)

        time.sleep(2)

    elif op == 3: # qnt de pessoas no condominio
        print "\nQnt TOTAL de pessoas no Condominio: " + str(lista_atual_qnt + lista_espera_qnt) + "\n\tPredio1 [ " + str(qnt_predio1) + " ]\tPredio2 [ " + str(qnt_predio2) + " ]"
        a = raw_input ("\nEnter para continuar...")
    
    elif op == 4: # qnt de pessoas dentro do condominio
        print "\nQnt de pessoas dentro do Condominio: " + str(lista_atual_qnt)
        a = raw_input ("\nEnter para continuar...")
    
    elif op == 5: # qnt de pessoas na lista de espera do condominio
        print "\nQnt de pessoas na lista de espera do Condominio: " + str(lista_espera_qnt)
        a = raw_input ("\nEnter para continuar...")
    
    elif op == 9: # reiniciar aplicacao
        dic = {0 : "reiniciar"}
        s.send(str(dic))
        resposta = s.recv()
        if resposta == "reiniciado":
            lista_atual_qnt, lista_espera_qnt, qnt_predio1, qnt_predio2 = 0, 0, 0, 0
            print "\n*************************************"
            print "| Aplicacao reiniciada com sucesso! |"
            print "*************************************\n"
        else:
            print "\nErro ao reiniciar aplicacao!\n"
        
        a = raw_input ("\nEnter para continuar...")
    
    elif op == 0: # sair
        controle = 0
        
    else:
        print "\nComando invalido, tente novamente!\n"
