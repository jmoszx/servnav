import mimetypes
import socket
import sys
from formataArgumentos import Parser



if __name__ == '__main__':
    #declaração de variáveis utilizadas. 
    timetoBind = 5
    timetoRead = 1    
    #utilizadas em timeout de conexões 

    dataRcv = b''    #uso objetos de bytes / usado pra receber os dados
    #utilizada no recebimento de bytes do socket
    
    flagSepara = b'\r\n\r\n' #flag usada na detecção de cabeçalho
    #utilizada para a análise de cabeçalho

    htmlCodigo = False #codigo de log HTML
    ref_htmlCodigo = False #referencia ao codigo HTTP
    content_type = False #tipo contedo
    #Utilizadas para reconhecimento dos arquivos e auxiliares ao Magic

    
    entradaArgs = sys.argv[1] #Faz a Leitura da entrada no teclado = entradaArgs
        
    parser = Parser()
    #Instancia o objeto para a classe Parser

    entradaEstruturada = parser.corrige_entrada(entradaArgs)#fornece o que foi lido pra ser estruturado.
    #Chama a funcao da classe Parser para estruturação dos argumentos recebidos

    SOURCE = entradaEstruturada['SOURCE']#Recurso é o item definido na busca
    PORT = entradaEstruturada['PORT']    #PORT é difinida a porta de acesso
    HOST = entradaEstruturada['ENDERECO']#HOST define o local acessado
                 
    #apos estruturação assinala a procura do recurso, a porta e o endereço
        
    if not entradaEstruturada: #caso não consiga ser estruturada informa invalidez e encerra.
        print('O endereço nao foi estruturado,entrada inválida.')
        sys.exit()
    


    print('\nO caminho',entradaArgs,' possui as diretrizes:')
    print('IP->', HOST,'porta', PORT)

    # estrutura de cabeçalho.
    formatCab = 'GET {0} HTTP/1.1\nHOST: {1}\nUser-Agent: Mozilla/5.0\n\n'.format(SOURCE, HOST).encode()

   	
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria novo socket
    try:
        socketTCP.settimeout(timetoBind) #limita tempo de conexão
        socketTCP.connect((HOST, PORT)) #conecta ao servidor através IP e PORTA
    except socket.timeout: #limite de tempo esgotado.
        print('\nServer, im not proud of u. U have a time!! \n')
        sys.exit()
    
    
    socketTCP.send(formatCab) #requisição é enviada através do socket  
    try:
        while True:
            socketTCP.settimeout(timetoRead) #limita tempo de leitira
            recebido = socketTCP.recv(2048) #recebe dados pelo Socket
            if not len(recebido):			
                break
            dataRcv = dataRcv + recebido
    except:
        print('')
        #caso atinja o time estabelecido 
        pass
    finally:
        socketTCP.close() #fecha socket

    if flagSepara not in dataRcv:
        flagSepara = b'\n\n'

    #Parcial Cabeçalho
    cabecalhoAtual = dataRcv.split(flagSepara)[0].decode() #cabecalho 
    arquivoConteudo = dataRcv[len(cabecalhoAtual) + len(flagSepara):] #conteudo do arquivo  

    for linha in cabecalhoAtual.splitlines():
        if not htmlCodigo:
            blocoCod = linha.strip().split(' ')
            htmlCodigo = blocoCod[1]
            ref_htmlCodigo = ' '.join(blocoCod[2:])
        if 'Content-Type' in linha:
            content_type = linha.split(':')[1].replace(' ', '').split(';')[0]
    try:
        ext = mimetypes.guess_extension(content_type) #assinala extensão do arquivo
    except:
        ext = '.html' #caso não, defina como HTML


    #print('REQUEST')
    print('Request code:', htmlCodigo, '({0})'.format(ref_htmlCodigo)) #printa o Status sobre codigo HTTP
    if SOURCE != '/':
        nome_arquivo = SOURCE.split('/')[-1].split('.')[0]
    else:
        nome_arquivo = entradaArgs.lstrip('http://').split('/')[0]
    
    with open(nome_arquivo + ext, 'wb') as arq:
        arq.write(arquivoConteudo)
    # Cria um arquivo e salva o conteudo transferido
    print('Arquivo Recebido', nome_arquivo + ext)
    print()