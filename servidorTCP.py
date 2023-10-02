import socket

HOST = '127.0.0.1'
PORT = 5000

# Criando um objeto do tipo socket
TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define um endereço e uma porta
server = (HOST, PORT)

# Iniciando a conexão do servidor
TCP.bind(server)
TCP.listen()
print('Aguardando conexao de um cliente no IP', HOST, 'na porta', PORT)

conexao, cliente = TCP.accept()
#print('\nConexão realizada por:', cliente)

while True:
    mensagem = conexao.recv(1024)
    if not mensagem:
        print('Fechando a conexao')
        conexao.close()
        break
    print('\nCliente:', cliente)
    print('Mensagem:', mensagem.decode())
    conexao.sendall(mensagem + b'\nMensagem recebida com sucesso!')



