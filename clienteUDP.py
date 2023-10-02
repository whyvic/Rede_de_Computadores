import socket

HOST = "127.0.0.1"
PORT = 5000

UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

destino = (HOST, PORT)

mensagem = input()

UDP.sendto(str.encode(mensagem), destino)

UDP.close()