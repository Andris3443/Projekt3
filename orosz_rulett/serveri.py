import socket
import threading
import random

HOST = "0.0.0.0"
PORT = 5555
running = True  # A szerver futásának vezérlése

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Szerver elindult... Várakozás kliensekre.")

clients = []
current_turn = 0  # Az aktuális játékos indexe (0 vagy 1)

def handle_client(client, player_id):
    global current_turn, running
    
    while running:
        try:
            data = client.recv(1024).decode()
            if not data:
                break
            
            if data == "FIRE":
                if player_id == current_turn:  # Csak a soron lévő játékos lőhet
                    random_number = random.randint(1, 6)
                    result = "DEAD" if random_number == 4 else "SAFE"
                    client.send(result.encode())
                    
                    # Következő játékos jön
                    current_turn = 1 - current_turn
                else:
                    client.send("NOT_YOUR_TURN".encode())  # Nem te jössz!
        except:
            break
    
    client.close()
    if client in clients:
        clients.remove(client)

def accept_clients():
    while running and len(clients) < 2:
        try:
            client, addr = server.accept()
            print(f"Kapcsolódott: {addr}")
            clients.append(client)
            threading.Thread(target=handle_client, args=(client, len(clients) - 1)).start()
        except:
            break

# Külön szálon futtatjuk a kliensek fogadását
client_thread = threading.Thread(target=accept_clients)
client_thread.start()

# Leállítás figyelése
while True:
    command = input("Írd be 'STOP' a szerver leállításához: ").strip()
    if command.upper() == "STOP":
        print("Szerver leállítása...")
        running = False
        break

# Összes kliens kapcsolatának bezárása
for client in clients:
    client.close()

server.close()
client_thread.join()
print("Szerver leállt.")
