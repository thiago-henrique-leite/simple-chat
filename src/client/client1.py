import sys
sys.path.append('../')

import PySimpleGUI as sg
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from scripts.sdes import SDES
from scripts.rc4 import RC4
from scripts.cbc import CBC
from scripts.diffie_helman import DiffieHelman

receiver, sender = '', ''

### Methods
def encrypt(message):
    if crypt_method == 'SDES': return SDES.encrypt(message, crypt_key)
    if crypt_method == 'RC4': return RC4.encrypt(message, crypt_key)
    if crypt_method == 'CBC': return CBC.encrypt(message, crypt_key)
    if crypt_method == 'DiffieHelman': return RC4.encrypt(message, crypt_key)

def decrypt(message):
    if crypt_method == 'SDES': return SDES.decrypt(message, crypt_key)
    if crypt_method == 'RC4': return RC4.decrypt(message, crypt_key)
    if crypt_method == 'CBC': return CBC.decrypt(message, crypt_key)
    if crypt_method == 'DiffieHelman': return RC4.decrypt(message, crypt_key)

def send_message():
  if not receiver == '' and not inputs['message'] == '':
    if not inputs['message'] == 'exit':
      client_socket.send(bytes(f"#{receiver}#{encrypt(inputs['message'])}", 'utf8'))

      messages.append(sender + ': ' + inputs['message'])
    else:
      client_socket.send(bytes('exit', 'utf8'))
      client_socket.close()
      window.close()

def publish_key():
  if not receiver == '' and not inputs['pubkey'] == '':
    client_socket.send(bytes(f"#pubkey#{receiver}#{inputs['pubkey']}", 'utf8'))

def receiver_public_key():
  try:
    print(f'receiver_public_key: {chaves_publicas[receiver]}')
    return chaves_publicas[receiver]
  except:
    return 0

def get_diffie_helman_key():
  DiffieHelman.get_key(private_key, receiver_public_key())

def add_public_key(host, key):
  print('')
  print('Atualizando chave pública:')
  print(f'Host: {host}')
  print(f'Chave: {key}')
  print('')
  print(f'add-pub: {host}')
  chaves_publicas[host] = key
  print(chaves_publicas)

def receive_message():
    while True:
        try:
            splited_message = client_socket.recv(1024).decode('utf8').split('#')
            print(splited_message)

            if len(splited_message) > 1:
              if splited_message[1] == sender:
                messages.append(f'{splited_message[0]}: {decrypt(splited_message[2])}')
              else:
                if not splited_message[0] == my_ip and splited_message[1] == 'pubkey':
                  add_public_key(splited_message[0], splited_message[3])
                  # crypt_key = get_diffie_helman_key()
            elif len(splited_message) == 1:
                messages.append(splited_message[0] + '\n')

            window['chat_messages'].update(values = messages)
        except:
            break

def set_name():
    client_socket.send(bytes(sender, 'utf8'))
###

port = 3001

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', port))

my_ip = '192.168.0.107'
to_ip = '192.168.0.17'

chaves_publicas = {}
chaves_publicas['192.168.0.17'] = 252
chaves_publicas['192.168.0.107'] = 253

private_key = 77
public_key = DiffieHelman.get_public(private_key)

print(public_key)

inputs, messages = [], []

crypts = ['SDES', 'RC4', 'CBC', 'DiffieHelman']
crypt_method, crypt_key = 'RC4', 'teste'

sg.change_look_and_feel('NeutralBlue')

color_boxes = 'red'

layout = [
    [sg.Text('Meu IP', size=(6,0)), sg.Input(my_ip, size=(21,0), key='sender'), sg.Text('IP', size=(2,0)), sg.Input(to_ip, size=(22,0), key='receiver'), sg.Button('Conectar', size=(10,0), key='connect')],
    [sg.Text('Criptografia', size=(10,0)), sg.OptionMenu(key='crypt', size=(10,0), values=crypts, default_value=crypts[1], text_color='black', pad=(10, 10)), sg.Text('Chave', size=(6,0)), sg.Input('teste', size=(18,0), key='key'), sg.Button('Atualizar', size=(10,0), key='update')],
    [sg.Text('Chave Privada', size=(12,0)), sg.Input(private_key, background_color=color_boxes, size=(14,0), key='privkey'), sg.Text('Chave Pública', size=(12,0)), sg.Input(public_key, background_color=color_boxes, size=(14,0), key='pubkey'), sg.Button('Publicar', size=(9,0), key='publish')],
    [sg.Listbox(key='chat_messages', size=(70,30), values=messages)],
    [sg.Text('Mensagem', size=(9,0)), sg.Input(size=(45,0), key='message', do_not_clear=False), sg.Button('Enviar', size=(10,0), key='send')],
]

window = sg.Window('SimpleChat with Python | @ThiagoLeite', layout, finalize=True)

receive_thread = Thread(target=receive_message)
receive_thread.start()

print('Chaves Públicas')
print(chaves_publicas)

while True:
  event, inputs = window.read()

  if event == sg.WINDOW_CLOSED:
    break

  if event == 'connect':
    sender = inputs['sender']
    receiver = inputs['receiver']
    set_name()

  if event == 'update':
    print("\n\nUPDATE\n\n")
    crypt_method = inputs['crypt']
    crypt_key = inputs['key']
    if crypt_method == 'DiffieHelman':
      color_boxes = 'green'
    else:
      color_boxes = 'red'
    window['pubkey'].update(background_color=color_boxes)
    window['privkey'].update(background_color=color_boxes)

  if event == 'publish':
    print("\n\nUPDATE\n\n")
    print(inputs['crypt'])
    if inputs['crypt'] == 'DiffieHelman':
      private_key = int(inputs['privkey'])
      print('passou')
      print(inputs['receiver'])
      print(chaves_publicas[inputs['receiver']])
      public_key = DiffieHelman.get_public(private_key)
      key = DiffieHelman.get_key(private_key, chaves_publicas[inputs['receiver']])
      window['pubkey'].update(public_key)
      window['key'].update(key)
      client_socket.send(bytes(f"#pubkey#{receiver}#{public_key}", 'utf8'))
      chaves_publicas[inputs['sender']] = public_key

  if event == 'send':
    send_message()
