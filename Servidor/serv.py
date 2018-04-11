import os
import socket
import sys
import magic
from processaRequisicao import *
from threading import Thread

enderecoIP = '127.0.0.1' #define padrão local para abertura do Socket.

with open('html/erro.html') as f:
	htmlErro = f.read()

with open('html/list.html') as f2:
	listarHtml = f2.read()


if __name__ == '__main__':
    path=''

    path = sys.argv[1]     	#recebe a entrada de argumentos
    PORT = int(sys.argv[2])
    reqProc = reqProcessa() #instancia a classe
    #print(path,PORT)
    # Checa se é um diretório válido
    if not os.path.isdir(path):
        print('Diretorio invalido')
        sys.exit()
        


    while True:
        #print('qq ta rolando')
        socketTCP = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #cria socket
        socketTCP.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          #porta pode utilizada mais de 1 vez
        try:
            socketTCP.bind((enderecoIP, PORT)) # tenta o bind
        except PermissionError:
            print('Porta sem permissão')
            sys.exit()
        socketTCP.listen(1)

        print('Servidor on {0}:{1}'.format(enderecoIP, PORT))

        conexao, info_cliente = socketTCP.accept()

        print('Client', ':'.join([str(i) for i in info_cliente]), '\n')
        Thread(target=reqProc.makeRequest, args=(conexao,path,listarHtml,htmlErro )).start() # Inicia a requisição em Threads