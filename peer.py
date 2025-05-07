import socket
import threading
import os
import pickle

SHARED_DIR = "shared"
DOWNLOAD_DIR = "downloads"
PORT = 5000

os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def list_shared_files():
    try:
        return os.listdir("shared")
    except FileNotFoundError:
        return []

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr} connected.")
    files = list_shared_files()
    conn.send(pickle.dumps(files))

    try:
        filename = conn.recv(1024).decode()
        path = os.path.join(SHARED_DIR, filename)
        if os.path.exists(path):
            with open(path, "rb") as f:
                while chunk := f.read(1024):
                    conn.send(chunk)
        else:
            print(f"[ERROR] File not found: {filename}")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", PORT))
    server.listen()
    print(f"[LISTENING] Peer is listening on port {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

def connect_to_peer(ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, PORT))

    data = client.recv(4096)
    files = pickle.loads(data)

    print(f"\nAvailable files from {ip}:\n")
    if not files:
        print("No files available.")
        return

    for idx, filename in enumerate(files, 1):
        print(f"{idx}. {filename}")

    try:
        choice = int(input("\nEnter file number to download: ")) - 1
        if 0 <= choice < len(files):
            client.send(files[choice].encode())
            with open(os.path.join(DOWNLOAD_DIR, files[choice]), "wb") as f:
                while True:
                    chunk = client.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"[DOWNLOADED] {files[choice]} saved to '{DOWNLOAD_DIR}'")
        else:
            print("Invalid file number.")
    except ValueError:
        print("Please enter a valid number.")

    client.close()

if __name__ == "__main__":
    mode = input("Run as server or client? ").strip().lower()
    if mode == "server":
        print("[STARTING SERVER]")
        start_server()
    elif mode == "client":
        while True:
            cmd = input("Enter peer IP to connect (or 'exit'): ").strip()
            if cmd.lower() == "exit":
                break
            try:
                connect_to_peer(cmd)
            except Exception as e:
                print(f"[ERROR] {e}")
    else:
        print("Invalid mode. Choose 'server' or 'client'.")
        