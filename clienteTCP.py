import socket

HOST = '127.0.0.1'
PORT = 5000

TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = (HOST, PORT)
TCP.connect(server)
TCP.sendall(str.encode('Ola, bom dia'))
mensagem = TCP.recv(1024)
print('Mensagem ecoada:', mensagem.decode())