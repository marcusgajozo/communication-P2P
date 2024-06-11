
# Receiver (Receptor)

Este script recebe um arquivo enviado por um remetente usando UDP.

## Requisitos

- Python 3.x

## Uso

```bash
python receiver.py -f <nome_do_arquivo>
```

## Argumentos

- `-f, --file`: Nome do arquivo a ser salvo.

## Funcionalidades

1. Recebe os dados do remetente.
2. Verifica se o arquivo já existe.
3. Cria um socket UDP.
4. Abre o arquivo para escrita.
5. Recebe os pacotes de dados e os salva no arquivo especificado.

---

# Sender (Remetente)

Este script envia um arquivo para um receptor usando UDP.

## Requisitos

- Python 3.x

## Uso

```bash
python sender.py -f <caminho_do_arquivo> -ht <endereço_host>
```

## Argumentos

- `-f, --file`: Caminho do arquivo a ser enviado.
- `-ht, --host`: Endereço host do receptor.

## Funcionalidades

1. Envia os dados para o receptor.
2. Define o sinal de alarme para lidar com timeouts.
3. Cria um socket UDP.
4. Determina o tamanho do arquivo.
5. Lê e envia o arquivo em pacotes de 100 bytes.
6. Aguarda pela confirmação (ACK) do receptor e retransmite em caso de timeout.

