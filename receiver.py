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

# recebe de qualquer endereço ip
sock.bind(("0.0.0.0", PORT_NUMBER))

# Abrindo o arquivo para escrita
with open(file_name, "wb") as file:
    # Recebendo e salvando os pacotes
    while True:
        packet, addr = sock.recvfrom(101)  # 100 bytes de dados + 1 byte de cabeçalho
        header = int(chr(packet[0]))
        if header == 0 or header == 1:
            data = packet[1:]  # 0
            ack = str(header + 2).encode()  # ACK = header + 2
            sock.sendto(ack, addr)
            if len(data) > 0:  # 90
                file.write(data)
                if len(data) < 100:
                    break
            else:
                break

print("Arquivo recebido com sucesso.")
sock.close()
