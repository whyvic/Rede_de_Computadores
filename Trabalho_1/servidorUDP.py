import socket

HOST = "127.0.0.1"
PORT = 5000

UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server = (HOST, PORT)
UDP.bind(server)
print('Aguardando conexao de um cliente cd IP', HOST, 'na porta', PORT)

while True:
    mensagem, cliente = UDP.recvfrom(1024)
    print('\nCliente:', cliente)
    print('Mensagem:', mensagem.decode())
    break
UDP.close()
