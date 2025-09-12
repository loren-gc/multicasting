# Sistema de Multicasting Ordenado

Implementação de um algoritmo de multicast totalmente ordenado para a disciplina de Sistemas Distribuídos, seguindo o modelo baseado em relógios lógicos e confirmações (acks).

## 📋 Descrição

Este projeto implementa um sistema de comunicação entre processos onde as mensagens são entregues na mesma ordem para todos os participantes. O algoritmo garante ordenação total das mensagens usando relógios lógicos de Lamport e confirmações de recebimento.

## ⚙️ Funcionalidades

- **Multicast ordenado**: Mensagens entregues na mesma ordem para todos os processos
- **Relógios lógicos**: Sincronização de eventos usando o algoritmo de Lamport
- **Confirmações (ACKs)**: Sistema de acks para garantir entrega ordenada
- **Tolerância a atrasos**: Funciona mesmo quando acks chegam antes das mensagens originais
- **Comunicação TCP**: Conexões confiáveis entre processos

## 🏗️ Estrutura do Projeto

    multicasting/
    ├── multicasting1.py # Processo com ID 0 (porta 5050)
    ├── multicasting2.py # Processo com ID 1 (porta 5051)
    ├── multicasting3.py # Processo com ID 2 (porta 5052)
    └── README.md


## 📦 Pré-requisitos

- Python 3.6 ou superior
- Nenhuma dependência externa necessária

## 🚀 Como Executar

1. **Abra três terminais diferentes**

2. **Execute cada processo em um terminal separado:**

```bash
# Terminal 1 - Processo 0
python3 multicasting1.py

# Terminal 2 - Processo 1  
python3 multicasting2.py

# Terminal 3 - Processo 2
python3 multicasting3.py
```

3. **Exemplo de configuração no multicasting1.py:**

```bash
id_processo = 0
portas_processos = [5051, 5052]  # Portas dos outros processos
port_server = 5050  # Sua própria porta
```
