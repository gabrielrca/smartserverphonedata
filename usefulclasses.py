class reading:
    sensID=''       #identificacao do telefone usado como sensor
    sensType=''     #Tipo do sensor ACC, GYR, LGT, MAG, RAWMAG, ORI, PRS, PRX
    timestamp=''    #Hora que o dado chegou
    desc=''         #descricao em texto sobre o que eh, onde esta localizado, etc
    ip=''           #Endereco IP do dispositivo
    port=''         #Porta TCP que o dispositivo usou pra se conectar
    numRead=''      #Numero que o aplicativo me manda (ainda nao sei o que eh)
    Acel =''        #valor da leitura do acelerometro - ACC
    Giros =''       #valor da leitura do giroscopio - GYR
    Luz =''         #valor da leitura de luminosidade - LGT
    MagField =''    #valor da leitura do campo magnetico - MAG
    MagFieldRaw ='' #valor da leitura do campo magnetico (RAW) - RAWMAG
    Orient =''      #valor de leitura da orientacao - ORI 
    Press =''       #valor de leitura de pressao - PRS 
    Prox =''        #valor do leitor de proximidade - PRX


class coordXYZ:
    x=''
    y=''
    z=''

class rawmagfields:
    a=''
    b=''
    c=''
    d=''
    e=''
    f=''

class orientationfields:
    a=''
    b=''
    c=''
    d=''

class timeOfReceive:
    dia=''
    mes=''
    ano=''
    hora=''
    minu=''
    seg=''
    micrsec=''