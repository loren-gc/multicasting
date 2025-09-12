import socket
import threading
import queue
import json
import time

# clock_local:
#       INCREMENTAR AO ENVIAR MENSAGEM OU ACK
#       iNCREMENTAR COM A OCORRÊNCIA DE EVENTOS

#########################################################################################################

lock = threading.Lock()

clock_local = 0
id_processo = 0

ip_geral = "127.0.0.1"
portas_processos = [5051, 5052]

ip_server = "127.0.0.1"
port_server = 5050+id_processo

#fila para a comunicação entre threads:
comunicacao_threads = queue.Queue()
fila_mensagens = queue.PriorityQueue()
fila_acks = queue.Queue()

################################################### FUNCOES #############################################

# ao receber um ack verificamos se existe uma mensagem pronta para ser entregue para a aplicação:
def aplicacao(ack):
    fila_acks.put(ack)
    prim_mensagem = fila_mensagens.get()
    if prim_mensagem[1]["id_unico"] != ack["id_unico"]:
        fila_mensagens.put(prim_mensagem)
        return
    qtd_acks = 1
    if ack["id_processo"] == id_processo:
        qtd_acks = 2
    #contar quantos acks relativos a mensagem cabeça de fila existem:
    acks_removidos = []
    tamanho = fila_acks.qsize()
    for _ in range(tamanho):
        item = fila_acks.get()
        if item["id_unico"] == prim_mensagem[1]["id_unico"]:
            qtd_acks -= 1
        acks_removidos.append(item)
    if qtd_acks == 0: #achamos todos os acks para a mensagem cabeça de fila
        print("\nMENSAGEM DO SERVIDOR PARA A APLICAÇÃO: "+prim_mensagem[1]["corpo"]+"\n")
    else:
        print("nao achamos todos os acks")
        fila_mensagens.put(prim_mensagem)
        for item in acks_removidos: #reinserindo os elementos na fila de acks
            fila_acks.put(item)
        return

def enviar_acks(id_unico, processo):
    global clock_local
    with lock:
        clock_local += 1
    ack = {
        'tipo': "ack",
        'clock': clock_local,
        'id_unico': id_unico,
        'id_processo': processo
    }
    payload = json.dumps(ack).encode("utf-8")
    
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((ip_geral, portas_processos[0]))
    s2.connect((ip_geral, portas_processos[1]))
    s1.sendall(payload)
    s2.sendall(payload)
    
def trata_mensagem(mensagem):
    if mensagem["tipo"] == "ack":
        aplicacao(mensagem)
    else:
        fila_mensagens.put((mensagem["clock"], mensagem))
        enviar_acks(mensagem["id_unico"], mensagem["id_processo"])
        
def manutencao_clock_local(clock_estrangeiro):
    global clock_local
    with lock:
        if clock_estrangeiro > clock_local:
            clock_local = clock_estrangeiro + 1
    
def trata_cliente(conn, addr):
    try:
        data = conn.recv(1024)
        mensagem = json.loads(data.decode("utf-8"))
        manutencao_clock_local(mensagem["clock"])
        trata_mensagem(mensagem)
    except json.JSONDecodeError:
        print(f"[{addr}] Erro: JSON inválido!")
        
def servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_server, port_server))
    server.listen()
    while True:
        conn, addr = server.accept()
        # thread para tratar o cliente:
        thread = threading.Thread(target=trata_cliente, args=(conn, addr), daemon=True)
        thread.start()

def cliente():
    while True:
        corpo = input("Digite a mensagem\n")
        global clock_local
        with lock:
            clock_local += 1
        mensagem ={
            'tipo': "mensagem",
            'clock': clock_local,
            'corpo': corpo,
            'id_unico': int(time.time() * 1000),    
            'id_processo': id_processo
        }
        payload = json.dumps(mensagem).encode("utf-8")
    
        s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s1.connect((ip_geral, portas_processos[0]))
        s2.connect((ip_geral, portas_processos[1]))
        s1.sendall(payload)
        s2.sendall(payload)
    
#################################################### MAIN ##################################################

if __name__ == "__main__":
    thread1 = threading.Thread(target=cliente)
    thread2 = threading.Thread(target=servidor)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

