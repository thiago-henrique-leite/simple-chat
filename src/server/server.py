from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

addresses, clients = {}, {}

server = socket(AF_INET, SOCK_STREAM)

PORT = 3001

server.bind(('localhost', PORT))

def thread_main():
    if __name__ == '__main__':
        print('Servidor Online 🔥')
        server.listen(5)
        thread = Thread(target=accept_new_connection)
        thread.start()
        thread.join()

    server.close()

def accept_new_connection():
    while True:
        client, address = server.accept()
        addresses[client] = address
        thread = Thread(target=process_new_connection, args=(client,))
        thread.start()

def process_new_connection(client):
    hostname = client.recv(1024).decode('utf8')
    client.send(bytes(hostname + ' está online', 'utf8'))
    send_message_to_all_clients(bytes(f'{hostname} entrou no chat', 'utf8'))
    clients[client] = hostname

    while True:
        message = client.recv(1024)

        if message == bytes('exit', 'utf8'):
            client.send(bytes('exit', 'utf8'))
            client.close()
            clients.pop(client)
            send_message_to_all_clients(bytes(f'{hostname} saiu do chat', 'utf8'))
            break

        send_message_to_all_clients(message, hostname)

def send_message_to_all_clients(message, host=''):
    for client in clients: client.send(bytes(host, 'utf8') + message)

thread_main()
