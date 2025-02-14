import threading
import queue
import time

class Process:
    def __init__(self, id):
        self.id = id
        self.neighbors = []  
        self.channels = {}  
        self.state = None  
        self.recorded_state = None
        self.recorded_channels = {}
        self.received_markers = set()
        self.lock = threading.Lock()

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self) 

            
            self.channels[neighbor] = queue.Queue()  
            neighbor.channels[self] = queue.Queue()  

            print(f"✅ [DEBUG] Processo {self.id} agora tem um canal exclusivo PARA {neighbor.id}")
            print(f"✅ [DEBUG] Processo {neighbor.id} agora tem um canal exclusivo PARA {self.id}")



    def send_message(self, neighbor, message):
        if neighbor in self.channels:
            neighbor.channels[self].put((self.id,message))
            print(f"Processo {self.id}: Enviando {message} para {neighbor.id}")
            print(f"[DEBUG] Fila de processo {neighbor.id}: {self.channels[neighbor].qsize()} mensagens")

    def receive_message(self, neighbor):
        try:
            sender_id, msg = self.channels[neighbor].get_nowait()
            print(f"[DEBUG] Fila de processo {self.id}: retirou '{msg}' da fila de {neighbor.id}")
            return sender_id, msg
        except queue.Empty:
            return None,None

    def record_state(self):

        print(f"[DEBUG] Processo {self.id}: Entrou no record_state!")

        if self.state is None:
            print(f"⚠️ [AVISO] Processo {self.id}: Estado ainda é None, não registrando!")
        else:
            print(f"[DEBUG] Processo {self.id}: Estado ANTES do registro = {self.state}")

        self.recorded_state = self.state  
        self.recorded_channels = {n.id: [] for n in self.neighbors}  
        print(f"[DEBUG] Processo {self.id}: ✅ Estado registrado = {self.recorded_state}")


    def receive_marker(self, sender):
        with self.lock:
            print(f"[DEBUG] Processo {self.id}: Recebido marcador de {sender.id}")

            if self.recorded_state is None:  
                print(f"Processo {self.id}: Registrando estado AGORA...")
                try:
                    self.record_state()
                except Exception as e:
                    print(f"Erro ao registrar estado: {e}")
                    return
                
                self.received_markers.add(sender)
                for neighbor in self.neighbors:
                    if neighbor != sender:
                        print(f"Processo {self.id}: Enviando marcador para {neighbor.id}")
                        self.send_message(neighbor, "MARKER")
            else:
                print(f"Processo {self.id}: Já recebeu marcador de {sender.id}")
                self.received_markers.add(sender)
            
            while not self.channels[sender].empty():
                msg = self.channels[sender].get()
                self.recorded_channels[sender.id].append(msg)
                print(f"[DEBUG] Processo {self.id}: Registrando '{msg}' de {sender.id}")

    def process_messages(self):

        while True:
            for neighbor in self.neighbors:
                sender_id, msg = self.receive_message(neighbor)
                if msg:
                    print(f"Processo {self.id}: Recebido {msg} de {sender_id}")

                if msg == "MARKER":
                    print (f"Processo {self.id}: Recebido marcador de {sender_id}")
                    self.receive_marker(neighbor)
                elif msg:
                    self.state = f"Processed {msg}"  
                    print(f"Processo {self.id}: Processado {msg}")
        

    def start(self):
        threading.Thread(target=self.process_messages, daemon=True).start()

def simulate_checkpointing():
    p1 = Process(1)
    p2 = Process(2)
    p3 = Process(3)

    p1.add_neighbor(p2)
    p1.add_neighbor(p3)
    p2.add_neighbor(p1)
    p2.add_neighbor(p3)
    p3.add_neighbor(p1)
    p3.add_neighbor(p2)

    processes = [p1, p2, p3]

    for p in processes:
        p.start()

    p1.send_message(p2, "Msg1")
    time.sleep(1)
    p2.send_message(p3, "Msg2")
    time.sleep(1)
    p3.send_message(p1, "Msg3")
    time.sleep(1)

    time.sleep(1)
    print("\nIniciando checkpointing...")
    p1.record_state()
    time.sleep(1)
    for neighbor in p1.neighbors:
        time.sleep(2)
        print(f"Processo {p1.id}: Enviando marcador para {neighbor.id}")
        p1.send_message(neighbor, "MARKER")
    

    time.sleep(2)

    for p in processes:
        print(f"Processo {p.id}: Estado registrado = {p.recorded_state}")
        print(f"Processo {p.id}: Canais registrados = {p.recorded_channels}")

simulate_checkpointing()
