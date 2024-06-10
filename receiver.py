import socket
import os
import argparse

from constants import PORT_NUMBER

# Configurando argumentos de linha de comando
parser = argparse.ArgumentParser(
    description="Recebe um arquivo enviado por um remetente usando UDP"
)
parser.add_argument(
    "-f", "--file", type=str, help="Nome do arquivo a ser salvo", required=True
)
args = parser.parse_args()

file_name = args.file

# Verificando se o arquivo já existe
if os.path.exists(file_name):
    print("Erro: O arquivo já existe.")
    exit()

# Criando o socket UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("localhost", PORT_NUMBER))

# Abrindo o arquivo para escrita
with open(file_name, "wb") as file:
    # Recebendo e salvando os pacotes
    sequence_number = 0
    while True:
        packet, addr = sock.recvfrom(101)  # 100 bytes de dados + 1 byte de cabeçalho
        header = int(chr(packet[0]))
        if sequence_number == header:
            data = packet[1:]
            # Enviando ACK
            ack = str(sequence_number + 2).encode()  # ACK = sequence_number + 2
            sock.sendto(ack, addr)
            if not data:
                break
            file.write(data)
            sequence_number = (sequence_number + 1) % 2

print("Arquivo recebido com sucesso.")
sock.close()
