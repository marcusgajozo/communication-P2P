import argparse
import os
import signal
import socket

from constants import PORT_NUMBER


# Função para lidar com o sinal de alarme
def handler(signum, frame):
    global last_packet
    print("Tempo limite expirado. Retransmitindo último pacote...")
    sock.sendto(last_packet, (host, PORT_NUMBER))
    signal.alarm(2)


# Definindo o sinal de alarme
signal.signal(signal.SIGALRM, handler)

# Configurando argumentos de linha de comando
parser = argparse.ArgumentParser(
    description="Envia um arquivo para um receptor usando UDP"
)
parser.add_argument(
    "-f", "--file", type=str, help="Caminho do arquivo a ser enviado", required=True
)
parser.add_argument(
    "-ht", "--host", type=str, help="Endereço host do receptor", required=True
)
args = parser.parse_args()

file_path = args.file
host = args.host

# Criando o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Determinando o tamanho do arquivo
file_size = os.path.getsize(file_path)

# Lendo e enviando o arquivo em pacotes de 100 bytes
with open(file_path, "rb") as file:
    sequence_number = 0
    while True:
        data = file.read(100)
        header = str(sequence_number).encode()
        packet = header + data
        last_packet = (
            packet  # Salva o último pacote para retransmissão em caso de timeout
        )
        sock.sendto(packet, (host, PORT_NUMBER))
        while True:
            signal.alarm(2)  # Define o alarme para 2 segundos
            ack = sock.recv(1)
            signal.alarm(0)  # Cancela o alarme
            res = str(sequence_number + 2).encode()  # resposta esperada
            if ack == res:
                break
            else:
                print("Erro: ACK inválido recebido.")
        sequence_number = (sequence_number + 1) % 2
        if len(data) < 100:
            break

print("Arquivo enviado com sucesso.")
sock.close()
