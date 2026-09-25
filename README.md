# 📦 Levantamento de Estoque

Sistema de levantamento de estoque desenvolvido para a disciplina de **Computação Distribuída**, utilizando **Arduino, Python e WebSockets**.

O projeto simula um processo de inventário no qual um Arduino detecta a leitura de um produto, o cliente realiza o sorteio do produto correspondente e mantém o levantamento durante a sessão. Ao finalizar, o cliente envia o levantamento para o servidor através de WebSocket, e o servidor apresenta o balancete no terminal.

---

## 🏗️ Arquitetura

## Arquitetura

O projeto é composto por um Arduino, um cliente Python, um servidor WebSocket e uma interface web.

```text
                        ┌─────────────────────┐
                        │     Funcionário     │
                        └──────────┬──────────┘
                                   │
                                   │ Leitura
                                   ▼
                        ┌─────────────────────┐
                        │       Arduino       │
                        └──────────┬──────────┘
                                   │ Serial
                                   ▼
                        ┌─────────────────────┐
                        │    Cliente Python   │
                        │      (Leitor)       │
                        └──────────┬──────────┘
                                   │
                                   │ WebSocket
                                   ▼
                  ┌────────────────────────────────┐
                  │       Servidor WebSocket       │
                  │            Tornado             │
                  └───────────────┬────────────────┘
                                  │
                                  │ WebSocket
                                  ▼
                  ┌────────────────────────────────┐
                  │         Interface Web          │
                  │                                │
                  │ index.html                     │
                  │ static/scripts/app.js          │
                  │ static/styles/style.css        │
                  └────────────────────────────────┘
                                  │
                                  │ Envia levantamento
                                  ▼
                  ┌────────────────────────────────┐
                  │       Servidor WebSocket       │
                  │                                │
                  │    Processa o levantamento     │
                  └────────────────────────────────┘
```

## 🚀 Execução do projeto

### Pré-requisitos

- Python 3.12+
- [UV](https://docs.astral.sh/uv/)
- Arduino UNO
- Sensor KY-032
- Arduino conectado ao computador via USB

### 1. Instalar as dependências

Na raiz do projeto, execute:

```bash
uv sync
```

### 2. Configurar a porta serial

Crie um arquivo `.env` na raiz do projeto:

```env
ESTOQUE_SERIAL_PORT=COM3
ESTOQUE_SERIAL_BAUDRATE=9600
ESTOQUE_DIR_DADOS=estoque/dados/produtos.json
```

> Altere `COM3` para a porta serial utilizada pelo Arduino.

### 3. Iniciar o servidor

Abra um terminal na raiz do projeto e execute:

```bash
uv run task run
```

O servidor ficará aguardando conexões WebSocket.

### 4. Iniciar o cliente

Abra um **segundo terminal**, também na raiz do projeto, e execute:

```bash
uv run task cli
```