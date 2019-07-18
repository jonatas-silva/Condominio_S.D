# bibliotecas utilizadas

import zmq
import ast # biblioteca usada para converter String em um Dicionario
from random import * # randint(0,9) , random.choice('abc') # Gera numeros aleatorios inteiros
import time
temporizador = 0 # [0] desabilitado, [1 ou mais] habilitado, quanto maior mais devagar


# REDE [ AWS - Jonatas da Silva Oliveira ]

GERENCIADOR_PUBLICO = "18.212.158.216"
GERENCIADOR_PRIVADO = "172.31.43.246"
PREDIO_PUBLICO = "54.162.185.55"

PREDIO_PRIVADO = "172.31.39.90"
ANDAR_PRIVADO = "172.31.81.46"
ANDAR2_PRIVADO = "172.31.81.255"
ANDAR3_PRIVADO = "172.31.87.59"


# REDE [ AWS - Rodrigo Nakamuta Izawa ]

PREDIO2_PUBLICO = "54.224.206.3"
PREDIO2_PRIVADO = "172.31.88.83"
ANDAR_PRIVADO2 = "172.31.84.251"
ANDAR2_PRIVADO2 = "172.31.80.195"
ANDAR3_PRIVADO2 = "172.31.80.100"


# LEGENDA PORTAS [   cliente   ->   servidor  ]

PORT1 = "5555" # [ cliente_app -> gerenciador ]
PORT2 = "5556" # [ cliente_adm -> server_predioX ] e ( [ gerenciador -> server_predioX ] sendo X = 1, 2 ou 3 )
PORT3 = "5557" # [ server_predioX -> server_andarY ] sendo X = 1, 2 ou 3    Y = 1, 2 ou 3