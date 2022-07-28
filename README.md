# Simple Chat with Python

Para utilizar o chat, execute os comandos abaixo em três terminais diferentes na raiz do projeto:

```bash
# Iniciando servidor
cd src/server && python3 server.py
```

```bash
# Iniciando cliente 01
cd src/client && python3 client.py <seu_ip> <ip_de_um_colega> <chave_privada>
cd src/client && python3 client.py 192.168.0.107 192.168.0.17 79
```

```bash
# Iniciando cliente 02
cd src/client && python3 client.py 192.168.0.17 192.168.0.107 63
```

Para executar os testes dos algoritmos de criptografia, execute os comandos abaixo:

```bash
cd tests && python3 -m unittest test_rc4.py
```

```bash
cd tests && python3 -m unittest test_sdes.py
```

```bash
cd tests && python3 -m unittest test_cbc.py
```

```bash
cd tests && python3 -m unittest test_diffie_helman.py
```
