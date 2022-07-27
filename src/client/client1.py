import sys
sys.path.append('../')

import PySimpleGUI as sg
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from scripts.sdes import SDES
from scripts.rc4 import RC4
from scripts.cbc import CBC
from scripts.diffie_helman import DiffieHelman

# Definição das variáveis globais

PORT = 3001
HOST = 'localhost'

# Quem recebe a mensagem e quem envia (você), respectivamente
RECEIVER, SENDER = '', ''

MY_IP = '192.168.0.107'
TO_IP = '192.168.0.17'

MY_PRIVATE_KEY = 79
MY_PUBLIC_KEY = DiffieHelman.get_public(MY_PRIVATE_KEY)

PUBLIC_KEYS_HASH = {}
PUBLIC_KEYS_HASH['192.168.0.17'] = 13
PUBLIC_KEYS_HASH['192.168.0.107'] = 12

inputs, messages = [], []

CRYPTS = ['SDES', 'RC4', 'CBC', 'DiffieHelman']
crypt_method, crypt_key = 'RC4', 'teste'

COLOR_BOXES = 'red'

# Interface gráfica do chat

sg.change_look_and_feel('NeutralBlue')

layout = [
    [sg.Text('Meu IP', size=(6,0)), sg.Input(MY_IP, size=(21,0), key='SENDER'), sg.Text('IP', size=(2,0)), sg.Input(TO_IP, size=(22,0), key='RECEIVER'), sg.Button('Conectar', size=(10,0), key='event_connect')],
    [sg.Text('Criptografia', size=(10,0)), sg.OptionMenu(key='crypt', size=(10,0), values=CRYPTS, default_value=CRYPTS[1], text_color='black', pad=(10, 10)), sg.Text('Chave', size=(6,0)), sg.Input('teste', size=(18,0), key='key'), sg.Button('Atualizar', size=(10,0), key='event_update')],
    [sg.Text('Chave Privada', size=(12,0)), sg.Input(MY_PRIVATE_KEY, background_color=COLOR_BOXES, size=(14,0), key='privkey'), sg.Text('Chave Pública', size=(12,0)), sg.Input(MY_PUBLIC_KEY, background_color=COLOR_BOXES, size=(14,0), key='pubkey'), sg.Button('Publicar', size=(9,0), key='event_publish')],
    [sg.Listbox(key='chat_messages', size=(70,30), values=messages)],
    [sg.Text('Mensagem', size=(9,0)), sg.Input(size=(45,0), key='message', do_not_clear=False), sg.Button('Enviar', size=(10,0), key='event_send')],
]

window = sg.Window('Chat with Encryption | @thiagoleite', layout, finalize=True)

# Métodos de criptografia

def encrypt(message):
    if crypt_method == 'SDES':
        return SDES.encrypt(message, crypt_key)
    if crypt_method == 'RC4':
        return RC4.encrypt(message, crypt_key)
    if crypt_method == 'CBC':
        return CBC.encrypt(message, crypt_key)
    if crypt_method == 'DiffieHelman':
        return RC4.encrypt(message, crypt_key)

def decrypt(message):
    if crypt_method == 'SDES':
        return SDES.decrypt(message, crypt_key)
    if crypt_method == 'RC4':
        return RC4.decrypt(message, crypt_key)
    if crypt_method == 'CBC':
        return CBC.decrypt(message, crypt_key)
    if crypt_method == 'DiffieHelman':
        return RC4.decrypt(message, crypt_key)

# Métodos de comunicação entre os clientes

def send_message():
    if RECEIVER != '' and inputs['message'] != '':
        if inputs['message'] != 'exit':
            client_socket.send(bytes(f"#{RECEIVER}#{encrypt(inputs['message'])}", 'utf8'))

            messages.append(f"{SENDER}: {inputs['message']}")
        else:
            client_socket.send(bytes('exit', 'utf8'))
            client_socket.close()
            window.close()

def receive_message():
    while True:
        try:
            splited_message = client_socket.recv(1024).decode('utf8').split('#')
            print(splited_message)

            splitted_message_size = len(splited_message)

            if splitted_message_size > 1:
                if splited_message[1] == SENDER:
                    messages.append(f'{splited_message[0]}: {decrypt(splited_message[2])}')
                else:
                    if splited_message[0] != SENDER and splited_message[1] == 'pubkey':
                        update_public_key(splited_message[0], splited_message[3])
            elif splitted_message_size == 1:
                messages.append(f"{splited_message[0]}\n")

            window['chat_messages'].update(values = messages)
        except:
            break

def publish_key():
    if RECEIVER != '' and inputs['pubkey'] != '':
        client_socket.send(bytes(f"#pubkey#{RECEIVER}#{inputs['pubkey']}", 'utf8'))

def update_public_key(host, key):
    print("\nAtualizando chave pública:")
    print(f'Host: {host}')
    print(f'Chave: {key}')

    PUBLIC_KEYS_HASH[host] = int(key)

    key = DiffieHelman.get_key(PUBLIC_KEYS_HASH[inputs['RECEIVER']], MY_PRIVATE_KEY)

    window['key'].update(key)

def connect_with_server():
    client_socket.send(bytes(SENDER, 'utf8'))

def crypt_is_diffie_helman():
    crypt_method == 'DiffieHelman'

def update_boxes_color_if_needed():
    if crypt_is_diffie_helman:
        COLOR_BOXES = 'green'
    else:
        COLOR_BOXES = 'red'

    window['pubkey'].update(background_color=COLOR_BOXES)
    window['privkey'].update(background_color=COLOR_BOXES)

def update_crypt_key_if_needed(inputs):
    if not crypt_is_diffie_helman: return

    MY_PRIVATE_KEY = int(inputs['privkey'])
    MY_PUBLIC_KEY = DiffieHelman.get_public(MY_PRIVATE_KEY)

    key = DiffieHelman.get_key(PUBLIC_KEYS_HASH[inputs['RECEIVER']], MY_PRIVATE_KEY)

    window['pubkey'].update(MY_PUBLIC_KEY)
    window['key'].update(key)

    client_socket.send(bytes(f"#pubkey#{RECEIVER}#{MY_PUBLIC_KEY}", 'utf8'))

    PUBLIC_KEYS_HASH[inputs['SENDER']] = MY_PUBLIC_KEY

    print(PUBLIC_KEYS_HASH)

# Iniciando conexão socket com o servidor na porta selecionada

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Iniciando thread para tratar o recebimento das mensagens

receive_thread = Thread(target=receive_message)
receive_thread.start()

while True:
    event, inputs = window.read()

    if event == sg.WINDOW_CLOSED: break

    if event == 'event_connect':
        SENDER, RECEIVER = inputs['SENDER'], inputs['RECEIVER']

        connect_with_server()

    if event == 'event_update':
        crypt_method, crypt_key = inputs['crypt'], inputs['key']

        update_boxes_color_if_needed()
        update_crypt_key_if_needed(inputs)

    if event == 'event_publish':
        update_crypt_key_if_needed(inputs)

    if event == 'event_send':
        send_message()
