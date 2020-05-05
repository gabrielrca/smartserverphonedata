import socket 
from _thread import *
import threading 
#from pymongo import MongoClient
import json, pprint
from usefulclasses import reading, coordXYZ, rawmagfields, orientationfields, timeOfReceive
import datetime

#criando a conexao e mantendo no banco para salvar os dados das leituras
#client = MongoClient('172.18.0.102')
#print(client.server_info())
#db=client['STORE_SENSORDATA']
#collection=db['sensordata']
#Fim do codigo que abre a conexao

  
print_lock = threading.Lock() 




def deviceDescription(deviceIP):
    #aqui eu retorno uma tupla ID, descricao
    #devo popular isso aqui a medida que mais sensores sao colocados no ambiente
    SensID = ''
    descr = ''

    if(deviceIP[0]=='192.168.1.231'):
        SensID = 'id_galaxyS3'
        descr = '2-prat-mesa'
    
    if(deviceIP[0]=='192.168.1.232'):
        SensID = 'id_motorolaAntigo'
        descr = '2-prat-porta'
    
    if(deviceIP[0]=='192.168.1.233'):
        SensID = 'id_galaxyS4'
        descr = 'cima-vitrola'
        
    return SensID, descr
  


def threaded(c, rcvAddr, leituraAnterior={}): #cria a variavel de leitura anterior pra soh salvar se as leituras foram diferentes e economizar espaco em disco
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
            thisReading.ACC = coord.__dict__
        
        if(fields[1] == 'GYR'):
            coord = coordXYZ() #cada campo da cordenada ta subsequente no campo de recebimento
            coord.x=fields[2]
            coord.y=fields[3]
            coord.z=fields[4]
            thisReading.GYR = coord.__dict__

        if(fields[1] == 'LGT'):
            thisReading.LGT = fields[2]

        if(fields[1] == 'MAG'):
            coord = coordXYZ() #cada campo da cordenada ta subsequente no campo de recebimento
            coord.x=fields[2]
            coord.y=fields[3]
            coord.z=fields[4]
            thisReading.MAG = coord.__dict__

        if(fields[1] == 'RAWMAG'):
             rawmagfiedsvalue = rawmagfields() #cada campo dos valores ta subsequente no campo de recebimento
             rawmagfiedsvalue.a = fields[2]
             rawmagfiedsvalue.b = fields[3]
             rawmagfiedsvalue.c = fields[4]
             rawmagfiedsvalue.d = fields[5]
             rawmagfiedsvalue.e = fields[6] 
             rawmagfiedsvalue.f = fields[7]
             thisReading.RAWMAG = rawmagfiedsvalue.__dict__
        

        if(fields[1] == 'ORI'):
            orientationvalues = orientationfields() #cada campo dos valroes ta subsequente no campo de recebimento
            orientationvalues.a = fields[2]
            orientationvalues.b = fields[3]
            orientationvalues.c = fields[4]
            orientationvalues.d = fields[5]
            thisReading.ORI = orientationvalues.__dict__

        if(fields[1] == 'PRS'):
            thisReading.PRS = fields[2] #valor do campo pressao

        if(fields[1] == 'PRX'):
            thisReading.PRX =  fields[2] #valor do campo proximidade
        

        leituraAnterior = salvarLeitura(thisReading.__dict__, leituraAnterior) #salvo a leitura no banco ou na console e guardo a leitura anterior
       
        

        
        if not dados: #aqui eu quebro o loop para fechar a conexao se nao tiver mais dados
            break
    
    c.close() #fecho a conexao

def salvarLeitura(leituraAtual, leituraAnterior):
    if(leituraAnterior == {}): #para salvar a primeira leitura, verifico se a leitura anterior ainda eh vazia
        print(leituraAtual) #salvo na console
        #collection.insert_one(thisReading.__dict__) #salvo no banco
        return leituraAtual
    elif(leituraAnterior['ip'] == leituraAtual['ip'] and leituraAnterior[leituraAnterior['sensType']] == leituraAtual[leituraAtual['sensType']]):
        #print('igual')
        #collection.insert_one(thisReading.__dict__)
        return leituraAtual #se for igual so retorno, nao salvo
    else:
        print(leituraAtual)
        #collection.insert_one(thisReading.__dict__)
        return leituraAtual


def print_debug(thing_to_print, debug): #funcao so para saber o que printar
    if(debug):
        print(thing_to_print)

  
def Main(): 
    host = "0.0.0.0" 
    port = 5555
    debug = False #Variavel para informar se vai fazer print das informacoes da aplicacao ou so dos dados

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #crio o socket
    s.bind((host, port))  #bindo o socket

 
    print_debug("socket bindado na porta " + str(port), debug) 
  
    s.listen(5) #escuto

    print_debug("ouvindo o socket", debug) 
  
    while True: 
  
        c, addr = s.accept() #aceitando conecao c com endereco addr

        

        print_debug('Conectado ao ip : ' + str(addr[0]) + ' na porta : ' + str(addr[1]), debug)   
        start_new_thread(threaded, (c, addr)) #envio a conexao e a tupla da conexao addr (ip, porta) pra ser tratado na thread

    s.close() 
  
if __name__ == '__main__': 
    Main() 


