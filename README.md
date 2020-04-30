# smartserverphonedata
Servidor em python criado para receber dados em stream de sensores de telefones celulares usando android através da aplicacao "Sensor Fusion"

A aplicação "Sensor Fusion" pode ser baixada na Play Store no link 

https://play.google.com/store/apps/details?id=com.hiq.sensor&hl=en

Essa aplicação permite enviar leituras dos sensores do celular em formato de stream para um servidor em uma porta TCP

## O que o código deste repositório faz é:
1. Receber as leituras do app "Sensor Fusion"
2. Tratar as leituras e formatar para salvar no banco
3. Adicionar campos de metadados para identificacao das leituras e do dispositivo que enviou
4. Salvar os dados coletados em um Mongo DB

## Exemplos de leituras que o app "Sensor Fusion" envia

- Acelerometro b'6200564\tACC\t-2.7006595\t6.0142345\t6.6367273\n'
- Giroscopio  b'6328404\tGYR\t0.005497787\t-0.053145275\t-0.0125227375\n'
- Luz  b'6350559\tLGT\t8.0\n'
- Campo Magnetico b'6367457\tMAG\t8.16\t4.68\t19.26\n'
- Campo Magnetico (raw)  b'6402289\tRAWMAG\t3.0\t-5.4\t26.939999\t-6.0\t5.94\t15.059999\n'
- Orientacao  b'6427494\tORI\t0.15982673\t0.30954745\t0.08656577\t-0.93334997\n'
- Pressao  b'6451856\tPRS\t1016.697\n'
- Proximidade  b'6480979\tPRX\t0.0\n' (PERTO) ou (LONGE) ('192.168.1.23', 56212) b'6481329\tPRX\t8.0\n'


O app também envia leituras de GPS e RSS, mas em meus testes nao recebi leituras de GPS, RSS (cell) e RSS (wifi).
