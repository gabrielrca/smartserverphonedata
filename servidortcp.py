#!/usr/bin/env python3

import socket

HOST = '0.0.0.0'  # Recebo de todas as interfaces
PORT = 555        # Fico escutando na porta 555, que é a porta que deve ser exposta no container

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) #abr socket no host e porta definidos anteriormente
    s.listen() #fico escutando meu socket

    conn, addr = s.accept() #conn eh a conexao e addr eh o endereco que se conectou

    with conn:
        print('Connected by', addr) #digo qual eh o aparelho que se conectou

        while True:
            data = conn.recv(1024) 
            print(data)
            #if not data:
            #    break
            #conn.sendall(data)
