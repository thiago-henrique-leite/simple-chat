import sys
sys.path.append('../')

import PySimpleGUI as sg
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from scripts.sdes import SDES
from scripts.rc4 import RC4

receiver, sender = '', ''

### Methods
def encrypt(message):
    if crypt_method == 'SDES': return SDES.encrypt(message, crypt_key)
    if crypt_method == 'RC4': return RC4.encrypt(message, crypt_key)

def decrypt(message):
    if crypt_method == 'SDES': return SDES.decrypt(message, crypt_key)
    if crypt_method == 'RC4': return RC4.decrypt(message, crypt_key)

def send_message():
  if not receiver == '' and not inputs['message'] == '':
    if not inputs['message'] == 'exit':
      client_socket.send(bytes(f"#{receiver}#{encrypt(inputs['message'])}", 'utf8'))

      messages.append(sender + ': ' + inputs['message'])
    else:
      client_socket.send(bytes('exit', 'utf8'))
      client_socket.close()
      window.close()

def receive_message():
    while True:
        try:
            splited_message = client_socket.recv(1024).decode('utf8').split('#')
            print(splited_message)

            if len(splited_message) > 1 and splited_message[1] == sender:
                messages.append(f'{splited_message[0]}: {decrypt(splited_message[2])}')
            elif len(splited_message) == 1:
                messages.append(splited_message[0])

            window['chat_messages'].update(values = messages)
        except:
            break

def set_name():
    client_socket.send(bytes(sender, 'utf8'))
###

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 3000))

my_ip = '192.168.0.17'
to_ip = '192.168.0.107'

inputs, messages = [], []

crypts = ['SDES', 'RC4']
crypt_method, crypt_key = 'RC4', 'teste'

sg.change_look_and_feel('NeutralBlue')

layout = [
  [sg.Text('Meu IP', size=(6,0)), sg.Input(my_ip, size=(20,0), key='sender'), sg.Text('IP', size=(2,0)), sg.Input(to_ip, size=(20,0), key='receiver'), sg.Button('Conectar', size=(10,0), key='connect')],
  [sg.Text('Criptografia', size=(10,0)), sg.OptionMenu(key='crypt', size=(8,0), values=crypts, default_value=crypts[1], text_color='black', pad=(10, 10)), sg.Text('Chave', size=(6,0)), sg.Input('teste', size=(20,0), key='key'), sg.Button('Atualizar', size=(10,0), key='update')],
  [sg.Listbox(key='chat_messages', size=(70,30), values=messages)],
  [sg.Text('Mensagem', size=(9,0)), sg.Input(size=(45,0), key='message', do_not_clear=False), sg.Button('Enviar', size=(10,0), key='send')],
]

window = sg.Window('SimpleChat with Python | @ThiagoLeite', layout, finalize=True)

receive_thread = Thread(target=receive_message)
receive_thread.start()

while True:
  event, inputs = window.read()

  if event == sg.WINDOW_CLOSED:
    break

  if event == 'connect':
    sender = inputs['sender']
    receiver = inputs['receiver']
    set_name()

  if event == 'update':
    crypt_method = inputs['crypt']
    crypt_key = inputs['key']

  if event == 'send':
    send_message()
