import socket 
from _thread import *
import threading 
from pymongo import MongoClient
import json, pprint
from usefulclasses import reading, coordXYZ, rawmagfields, orientationfields, timeOfReceive
import datetime

#criando a conexao e mantendo no banco para salvar os dados das leituras
client = MongoClient('172.18.0.102')
#print(client.server_info())
db=client['STORE_SENSORDATA']
collection=db['sensordata']
#Fim do codigo que abre a conexao

  
print_lock = threading.Lock() 

def deviceDescription(deviceIP):
    #aqui eu retorno uma tupla ID, descricao
    #devo popular isso aqui a medida que mais sensores sao colocados no ambiente
    SensID = ''
    descr = ''

    if(deviceIP[0]=='192.168.1.231'):
        SensID = 'id_galaxyS3'
        descr = 'Mesa do meu quarto embaixo da tela'
        
    return SensID, descr
  

def threaded(c, rcvAddr):
    #o objetivo dessa thread eh receber os dados e tratar e futuramente salvar no banco 
    while True: 
        
        #recebo e printo os dados
        dados = c.recv(1024)
        #print(rcvAddr, dados) 
        thisReading = reading() #thisReading eh o objeto que vai guardar os dados

        thisReading.ip = rcvAddr[0]
        thisReading.port= rcvAddr[1]

        thisReading.sensID, thisReading.desc = deviceDescription(rcvAddr) #pego o id e a descricao que eu defini
        
        fields = dados.decode().split() #pega as leituras, faz decode e splita em campos e joga na variavel fields

        #------Guardando o timestamp ------
        tr=timeOfReceive()
        horaQueRecebeu=datetime.datetime.now()
        tr.ano = horaQueRecebeu.year
        tr.mes = horaQueRecebeu.month
        tr.dia = horaQueRecebeu.day
        tr.hora = horaQueRecebeu.hour
        tr.minu = horaQueRecebeu.minute
        tr.seg = horaQueRecebeu.second
        tr.micrsec = horaQueRecebeu.microsecond
        thisReading.timestamp = tr.__dict__
        #--- FIM do Guardando o timestamp-----

        thisReading.numRead=fields[0] #campo 0 eh um numero que ele me passa
        thisReading.sensType=fields[1]  #pega o tipo de sensor ACC, GYR, LGT, MAG, RAWMAG, ORI, PRS, PRX

        if(fields[1] == 'ACC'):
            coord = coordXYZ() #cada campo da cordenada ta subsequente no campo de recebimento
            coord.x=fields[2]
            coord.y=fields[3]
            coord.z=fields[4]
            thisReading.Acel = coord.__dict__
        
        if(fields[1] == 'GYR'):
            coord = coordXYZ() #cada campo da cordenada ta subsequente no campo de recebimento
            coord.x=fields[2]
            coord.y=fields[3]
            coord.z=fields[4]
            thisReading.Giros = coord.__dict__

        if(fields[1] == 'LGT'):
            thisReading.Luz = fields[2]

        if(fields[1] == 'MAG'):
            coord = coordXYZ() #cada campo da cordenada ta subsequente no campo de recebimento
            coord.x=fields[2]
            coord.y=fields[3]
            coord.z=fields[4]
            thisReading.MagField = coord.__dict__

        if(fields[1] == 'RAWMAG'):
             rawmagfiedsvalue = rawmagfields() #cada campo dos valores ta subsequente no campo de recebimento
             rawmagfiedsvalue.a = fields[2]
             rawmagfiedsvalue.b = fields[3]
             rawmagfiedsvalue.c = fields[4]
             rawmagfiedsvalue.d = fields[5]
             rawmagfiedsvalue.e = fields[6] 
             rawmagfiedsvalue.f = fields[7]
             thisReading.MagFieldRaw = rawmagfiedsvalue.__dict__
        

        if(fields[1] == 'ORI'):
            orientationvalues = orientationfields() #cada campo dos valroes ta subsequente no campo de recebimento
            orientationvalues.a = fields[2]
            orientationvalues.b = fields[3]
            orientationvalues.c = fields[4]
            orientationvalues.d = fields[5]
            thisReading.Orient=orientationvalues.__dict__

        if(fields[1] == 'PRS'):
            thisReading.Press = fields[2] #valor do campo pressao

        if(fields[1] == 'PRX'):
            thisReading.Prox= fields[2] #valor do campo proximidade
        
        #print(thisReading.__dict__)
        collection.insert_one(thisReading.__dict__)
        

        
        if not dados: #aqui eu quebro o loop para fechar a conexao se nao tiver mais dados
            break
    
    c.close() #fecho a conexao
  
  
def Main(): 
    host = "0.0.0.0" 
    port = 555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crio o socket
    s.bind((host, port))  #bindo o socket

    print("socket bindado na porta", port) 
  
    s.listen(5) #escuto

    print("ouvindo o socket") 
  
    while True: 
  
        c, addr = s.accept() #aceitando conecao c com endereco addr

        

        print('Conectado ao ip :', addr[0], ' na porta :', addr[1])   
        start_new_thread(threaded, (c, addr)) #envio a conexao e a tupla da conexao addr (ip, porta) pra ser tratado na thread

    s.close() 
  
if __name__ == '__main__': 
    Main() 


'''
Exemplos de leituras
Acelerometro ('192.168.1.23', 37290) b'6200564\tACC\t-2.7006595\t6.0142345\t6.6367273\n'
Giroscopio ('192.168.1.23', 38247) b'6328404\tGYR\t0.005497787\t-0.053145275\t-0.0125227375\n'
Luz ('192.168.1.23', 49436) b'6350559\tLGT\t8.0\n'
Campo Magnetico ('192.168.1.23', 58082) b'6367457\tMAG\t8.16\t4.68\t19.26\n'
Campo Magnetico (raw) ('192.168.1.23', 53522) b'6402289\tRAWMAG\t3.0\t-5.4\t26.939999\t-6.0\t5.94\t15.059999\n'
Orientacao ('192.168.1.23', 55044) b'6427494\tORI\t0.15982673\t0.30954745\t0.08656577\t-0.93334997\n'
Pressao ('192.168.1.23', 50803) b'6451856\tPRS\t1016.697\n'
Proximidade ('192.168.1.23', 56212) b'6480979\tPRX\t0.0\n' (PERTO) ou (LONGE) ('192.168.1.23', 56212) b'6481329\tPRX\t8.0\n'
Nao vi leituras em GPS, RSS (cell) e RSS (wifi)
'''