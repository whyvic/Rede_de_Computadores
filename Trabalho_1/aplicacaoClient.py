import threading
import socket
import sys

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except ConnectionRefusedError:
        print('\nNão foi possível se conectar ao servidor. Certifique-se de que o servidor está em execução.\n')
        return
    except Exception as e:
        print(f'\nErro ao conectar ao servidor: {str(e)}\n')
        return

    print("*****************************************************************************")
    username = input('Digite seu nome: ')
    print(f'\nConectado como {username}.\n')
    print("*****************************************************************************")

    # Envie o nome do usuário para o servidor
    client.send(username.encode('utf-8'))


    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            if not msg:
                print('\nConexão perdida com o servidor.\n')
                client.close()
                sys.exit()  # Encerra o cliente
                break
            print(msg+'\n')
        except Exception as e:
            client.close()
            sys.exit()  # Encerra o cliente
            break

def sendMessages(client, username):
    while True:
        try:
            menu = """
            Menu de Comandos:
            Escolha o número referente à opção desejada:
            1 - CONSULTA
            2 - HORA
            3 - LISTAR
            4 - SAIR
            """

            print(menu)
            opcao = input("Digite o número do comando desejado: ")

            command_dispatcher = {
                '1': send_consulta,
                '2': send_hora,
                '3': send_listar,
                '4': send_sair
            }

            function = command_dispatcher.get(opcao, send_desconhecido)
            function(client)
        except Exception as e:
            print(f'\nErro ao enviar mensagem: {str(e)}\n')
            return

def send_consulta(client):
    client.send('CONSULTA'.encode('utf-8'))
    print()
def send_hora(client):
    client.send('HORA'.encode('utf-8'))
    print()

def send_listar(client):
    client.send('LISTAR'.encode('utf-8'))
    print()

def send_sair(client):
    try:
        client.send('SAIR'.encode('utf-8'))
        client.close()
        sys.exit()
    except Exception as e:
        print(f'\nErro ao encerrar a conexão: {str(e)}\n')
        sys.exit()

def send_desconhecido(client):
    print('\nComando desconhecido. Escolha um número válido do menu.')

main()
