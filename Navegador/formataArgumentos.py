import mimetypes
import socket
import sys


#Classe criada para realizar o parser da url.
class Parser(object):
	def __init__(self):
		super(Parser, self).__init__()
		# self.arg = arg

	def corrige_entrada(self, entrada): #Define a Formatação de ENTRADA
		argsEntrada = {'ENDERECO': '','PORT': 80,'SOURCE': '/'} #previamente set port 80
		#print(entrada)
		entrada = entrada.lstrip('http://') 
		entrada = entrada.lstrip('https://')
		#Feito o cut na string, removendo os termos dentre parenteses da string
		entrada = entrada.replace('/:', ':')
		#remove a barra final 
		paths = entrada.split('/') #caminhos ou diretórios
		dominio = entrada.split('/')[0] #source final ou caminho até o diretorio final 
		#Faz a seleção dos paths e o sources solicitado 

		
		if ':' in dominio:
			argsEntrada['PORT'] = int(dominio.split(':')[-1])
			dominio = dominio.split(':')[0]
			#Verifica se na entrada está alguma porta especificada se sim associa = PORT
		
		try:
			argsEntrada['ENDERECO'] = socket.gethostbyname(dominio) # obtem IP
		except:\
			return {}

		# search (arquivo)
		if len(paths) > 1:
			argsEntrada['SOURCE'] = '/' + '/'.join(entrada.split('/')[1:])

		return argsEntrada		