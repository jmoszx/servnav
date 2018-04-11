import os
import socket
import sys
import magic
from threading import Thread

class reqProcessa(object):
	def __init__(self):
		super(reqProcessa, self).__init__()
		# self.arg = arg
	def makeRequest(self,conexao, path, listarHtml, htmlErro):
	

	    requisicao = conexao.recv(2048).decode()
	    requestHandler = False  #declarado inicialmente como false o inicio da requisição
	    buildRequisicao = {}	  #campos de conferencia da requisiçao
	    bufferSaida = 1024 # necessario para envio do conteúdo pelo socket
	    hmtlCodigo = ''
	    ref_htmlCodigo = ''
	    content_type = ''
	    #inicia as variaveis utilizadas no processamento do cabeçalho 
	    
	    #inicia a requisição coletando seus componentes e os parametros dos componentes.
	    for line in requisicao.split('\n'):
	        if not requestHandler:
	            requestHandler = line
	            continue
	        itensCabecalho = line.strip('\r').split(':')[0]
	        paramItens = ':'.join(line.strip('\r').split(':')[1:]).strip()
	        buildRequisicao[itensCabecalho] = paramItens
	        #print(itensCabecalho)

	    try:
	        httpGET, source, httpVER = requestHandler.split(' ')
	    except ValueError:
	        httpGET = 'GET'
	        httpVER = 'HTTP/1.1'
	        source = '/'

	    
	    sourcePath = (path + source).replace('//', '/') #recurso ou diretorio

	    if os.path.isfile(sourcePath):
	        
	        hmtlCodigo = '200'
	        ref_htmlCodigo = 'ok'
	        retornoConteudo = '<h1> 200 ok</h1>'
	        content_type = 'text/html'
	        #define as variaveis inicializada caso sucesso
	        mime = magic.Magic(mime=True) 			#faz a magica do mime type
	        content_type = mime.from_file(sourcePath)	        
	        retornoConteudo = open(sourcePath, 'rb').read() # abre arquivo e le
	    

	    #Verifica se eh um diretorio, se for um diretorio .. faz a itemLista ..
	    elif os.path.isdir(sourcePath):
	        itemLista = ''
	        #para cada elemento deste diretorio, lista o item
	        for i in os.listdir(sourcePath):
	            itemLista += '<div class="listall">'
	            if not os.path.isdir(path+i): #faz chamada  do icone de arquivo caso seja arquivo.
	                itemLista += '<img src="https://image.freepik.com/free-icon/ico-file-format-variant_318-45749.jpg" width="15px" height="15px"><a href="' + source.rstrip('/') + '/' + i + '">' + i + '</a></img>'
	            else: #faz chama do icone de pasta caso seja diretorio
	                itemLista += '<img src="http://icons.iconseeker.com/ico/aruzo-dark-blue/folder-blue-12.ico" width="15px" height="15px"><a href="' + source.rstrip('/') + '/' + i + '">' + i + '</a></img>'
	            itemLista += '</div>'
	        retornoConteudo = listarHtml.format('SERVER ' + sourcePath,itemLista,'<a href="../"><img src="http://icons.iconseeker.com/ico/aruzo-dark-blue/folder-blue-12.ico" width="15px" height="15px">..</img></a>' if sourcePath.rstrip('/') != path.rstrip('/') else '')
	    else: #caso não seja o diretorio ou arquivo não existe e atribui 404 e retorna HTMLx
	        hmtlCodigo = '404'
	        ref_htmlCodigo = 'Not Found'
	        retornoConteudo = htmlErro
	    cabecalhoRetorno = 'HTTP/1.1 {0} {1}\nContent-Type: {2}\n\n'.format(hmtlCodigo,ref_htmlCodigo,content_type)

	    conexao.send(cabecalhoRetorno.encode()) # Faz o retorno de envio do cabeçalho

	    if isinstance(retornoConteudo, str):# Codifica o conteúdo para retorno seja feito, possibilita o reconhecimento de diretório.
	        retornoConteudo = retornoConteudo.encode()

	    for i in range(0, len(retornoConteudo), bufferSaida):
	        try:
	            conexao.send(retornoConteudo[i:i + bufferSaida])
	        except BrokenPipeError:
	            pass
	    #faz o envio atraves do socket 	    
	    conexao.close() #fecha conexão