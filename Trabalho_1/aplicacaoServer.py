import threading
import socket
import os
import time

clients = {}
client_usernames = {}

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except Exception as e:
        print(f'\nErro ao iniciar o servidor: {str(e)}\n')
        return

    print('Servidor está esperando conexões...')

    while True:
        try:
            client, addr = server.accept()
            client_ip = addr[0]
            client_port = addr[1]

            #client.send('Digite seu nome: '.encode('utf-8'))
            username = client.recv(2048).decode('utf-8')

            clients[username] = client
            client_usernames[client] = username


            print('-------------------------------------------------------------------------------')
            print(f'\nConexão realizada por: {client_ip}:{client_port}')
            print(f'Cliente {username} conectado.')
            print('-------------------------------------------------------------------------------')


            thread = threading.Thread(target=messagesTreatment, args=[client, username])
            thread.start()
        except Exception as e:
            print(f'\nErro ao aceitar conexão: {str(e)}\n')

def messagesTreatment(client, username):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if not msg:
                print(f'\nConexão perdida com {username}.\n')
                deleteClient(client, username)
                break
            if msg.upper() == 'CONSULTA':
                response = 'Informações do servidor'
                client.send(response.encode('utf-8'))
            elif msg.upper() == 'HORA':
                current_time = time.strftime("%H:%M:%S", time.localtime())
                response = f'HORA ATUAL {current_time}'
                client.send(response.encode('utf-8'))
            elif msg.startswith('ARQUIVO '):
                filename = msg.split(' ')[1]
                if os.path.exists(filename):
                    with open(filename, 'r') as file:
                        file_content = file.read()
                        response = f'ARQUIVO {filename} {file_content}'
                        client.send(response.encode('utf-8'))
                else:
                    client.send('ARQUIVO NAO ENCONTRADO'.encode('utf-8'))
            elif msg.upper() == 'LISTAR':
                files = os.listdir()
                file_list = ' '.join(files)
                response = f'LISTA DOS ARQUIVOS {file_list}'
                client.send(response.encode('utf-8'))
            elif msg.upper() == 'SAIR':
                #client.send('ADEUS'.encode('utf-8'))
                deleteClient(client, username)
                print('-------------------------------------------------------------------------------')

                print(f'Cliente {username} desconectado.')
                print()
                print('-------------------------------------------------------------------------------')

                break
            else:
                client.send('COMANDO DESCONHECIDO'.encode('utf-8'))
        except Exception as e:
            deleteClient(client, username)
            print(f'Cliente {username} desconectado.')
            break

def deleteClient(client, username):
    del clients[username]
    del client_usernames[client]

main()
