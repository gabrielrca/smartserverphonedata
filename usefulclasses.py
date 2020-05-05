class reading:
    sensID=''       #identificacao do telefone usado como sensor
    sensType=''     #Tipo do sensor ACC, GYR, LGT, MAG, RAWMAG, ORI, PRS, PRX
    timestamp=''    #Hora que o dado chegou
    desc=''         #descricao em texto sobre o que eh, onde esta localizado, etc
    ip=''           #Endereco IP do dispositivo
    port=''         #Porta TCP que o dispositivo usou pra se conectar
    numRead=''      #Numero que o aplicativo me manda (ainda nao sei o que eh)
    ACC =''          #valor da leitura do acelerometro - ACC
    GYR =''         #valor da leitura do giroscopio - GYR
    LGT =''         #valor da leitura de luminosidade - LGT
    MAG =''         #valor da leitura do campo magnetico - MAG
    RAWMAG =''      #valor da leitura do campo magnetico (RAW) - RAWMAG
    ORI =''         #valor de leitura da orientacao - ORI 
    PRS =''         #valor de leitura de pressao - PRS 
    PRX =''        #valor do leitor de proximidade - PRX


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