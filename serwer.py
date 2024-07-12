import socket
import struct
import threading
import time
import mysql.connector

class Client:
    def __init__(self, socket, username):
        self.socket = socket
        self.username = username

active_clients = []

        
def handle_client(client):
    try:
        # Odczekaj chwilę, aby klient zdążył odebrać nazwę użytkownika
        time.sleep(1)

        while True:

            length = client.socket.recv(4)
            mess_len = client.socket.recv(4)

            mess_len = int.from_bytes(mess_len, byteorder='big')
            length = int.from_bytes(length, byteorder='big')
                
            received_data = b""
            while len(received_data) < mess_len:
                tmp =client.socket.recv(1024)
                if not tmp:
                    break
                received_data += tmp


            if not received_data:
                break

            print(f"{client.username}: {received_data}")

            print(type(received_data))
            # Przesyłaj wiadomość do wszystkich klientów
            broadcast(length, len(received_data), received_data , client)
    except Exception as e:
        print(f"Błąd obsługi klienta {client.username}: {e}")
    finally:
        active_clients.remove(client)
        client.socket.close()


def broadcast(le, me_le, message, sender_client):
    chunk_size = 1024

    for other_client in active_clients:
        if other_client != sender_client:
            try:
                other_client.socket.send(le.to_bytes(4, byteorder='big'))
                other_client.socket.send(me_le.to_bytes(4, byteorder='big'))
                
                print(message)
                # Wysyłanie wiadomości partiami
                for i in range(0, me_le, chunk_size):
                    chunk = message[i:i+chunk_size]
                    other_client.socket.send(chunk)

            except Exception as e:
                print(f"Błąd podczas wysyłania do klienta {other_client.username}: {e}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.100.30', 12345))
    server.listen(5)

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kom"
    )

    print("Serwer nasłuchuje na porcie 12345...")

    cursor = db.cursor()

    while True:
        client_socket, addr = server.accept()
        print(f"Połączono z {addr[0]}:{addr[1]}")

        # Odbierz nazwę użytkownika od klienta
        username = client_socket.recv(1024).decode('utf-8')
        print(username)
        password = client_socket.recv(1024).decode('utf-8')
        print(password)

        querry = f"SELECT * FROM users WHERE login=\"{username}\" and pass=\"{password}\""
        cursor.execute(querry)
        results = cursor.fetchall()
        print(results)

        if len(results) < 1 or results[0][1] in [x.username for x in active_clients]:
            continue

        client = Client(client_socket, username)
        active_clients.append(client)

        
        header = struct.pack(f"!5s{len("Serwer")}s", "TEXT ".encode('utf-8'), "Serwer".encode("utf-8"))
        message = header + f"Witaj {client.username}".encode('utf-8')

        client.socket.send(len(header).to_bytes(4, byteorder='big'))
        client.socket.send(len(message).to_bytes(4, byteorder='big'))

        client.socket.send(message)


        header = struct.pack(f"!5s{len(client.username)}s", "TEXT ".encode('utf-8'), username.encode("utf-8"))

        message = header + "Połączono".encode('utf-8')
        
        broadcast(len(header), len(message), message, client)

        handle_thread = threading.Thread(target=handle_client, args=(client,))
        handle_thread.start()

start_server()
