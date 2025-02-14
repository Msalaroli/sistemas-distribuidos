# Sistemas Distribuídos

Este projeto implementa um sistema distribuído simples com processos que se comunicam entre si e realizam checkpointing para registrar seus estados.

## Descrição

O código define uma classe `Process` que representa um processo em um sistema distribuído. Cada processo pode enviar e receber mensagens de seus vizinhos e registrar seu estado e os estados dos canais de comunicação durante o checkpointing.

### Funcionalidades

- **Adicionar Vizinhos**: Cada processo pode adicionar vizinhos e criar canais de comunicação exclusivos com eles.
- **Enviar Mensagens**: Processos podem enviar mensagens para seus vizinhos.
- **Receber Mensagens**: Processos podem receber mensagens de seus vizinhos.
- **Registrar Estado**: Processos podem registrar seu estado atual e os estados dos canais de comunicação.
- **Receber Marcadores**: Processos podem receber marcadores para iniciar o processo de checkpointing.

## Estrutura do Código

- `Process`: Classe que representa um processo no sistema distribuído.
  - `__init__(self, id)`: Inicializa um processo com um ID.
  - `add_neighbor(self, neighbor)`: Adiciona um vizinho e cria um canal de comunicação.
  - `send_message(self, neighbor, message)`: Envia uma mensagem para um vizinho.
  - `receive_message(self, neighbor)`: Recebe uma mensagem de um vizinho.
  - `record_state(self)`: Registra o estado atual do processo e dos canais de comunicação.
  - `receive_marker(self, sender)`: Recebe um marcador e inicia o processo de checkpointing.
  - `process_messages(self)`: Processa mensagens recebidas dos vizinhos.
  - `start(self)`: Inicia a thread para processar mensagens.

- `simulate_checkpointing()`: Função que simula o processo de checkpointing entre três processos.

## Como Executar

1. Certifique-se de ter o Python instalado em seu sistema.
2. Salve o código em um arquivo chamado `SistemasDistribuidos.py`.
3. Execute o arquivo com o comando:
   ```sh
   python SistemasDistribuidos.py
   ```

## Exemplo de Saída

Ao executar o código, você verá a saída no console mostrando as mensagens enviadas e recebidas pelos processos, bem como os estados registrados durante o checkpointing.

```plaintext
Processo 1: Enviando Msg1 para 2
Processo 2: Recebido Msg1 de 1
Processo 2: Enviando Msg2 para 3
Processo 3: Recebido Msg2 de 2
Processo 3: Enviando Msg3 para 1
Processo 1: Recebido Msg3 de 3

Iniciando checkpointing...
Processo 1: Estado registrado = Processed Msg3
Processo 1: Enviando marcador para 2
Processo 1: Enviando marcador para 3
Processo 2: Recebido marcador de 1
Processo 2: Registrando estado AGORA...
Processo 2: Estado registrado = Processed Msg1
Processo 2: Enviando marcador para 3
Processo 3: Recebido marcador de 1
Processo 3: Registrando estado AGORA...
Processo 3: Estado registrado = Processed Msg2
Processo 3: Enviando marcador para 2

Processo 1: Estado registrado = Processed Msg3
Processo 1: Canais registrados = {2: [], 3: []}
Processo 2: Estado registrado = Processed Msg1
Processo 2: Canais registrados = {1: [], 3: []}
Processo 3: Estado registrado = Processed Msg2
Processo 3: Canais registrados = {1: [], 2: []}
```
```