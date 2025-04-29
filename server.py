import os
import socket
import threading

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

if not os.path.exists(SERVER_DATA_PATH):
    os.mkdir(SERVER_DATA_PATH)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK@Welcome to the File Server.".encode(FORMAT))

    while True:
        try:
            data = conn.recv(SIZE).decode(FORMAT)
            if not data:
                break
            data = data.split("@")
            cmd = data[0]

            if cmd == "LIST":
                files = os.listdir(SERVER_DATA_PATH)
                send_data = "OK@"
                if len(files) == 0:
                    send_data += "The server directory is empty."
                else:
                    send_data += "\n".join(f for f in files)
                conn.send(send_data.encode(FORMAT))

            elif cmd == "UPLOAD":
                name, text = data[1], data[2]
                filepath = os.path.join(SERVER_DATA_PATH, name)
                with open(filepath, "w") as f:
                    f.write(text)
                conn.send("OK@File uploaded successfully.".encode(FORMAT))

            elif cmd == "DELETE":
                files = os.listdir(SERVER_DATA_PATH)
                filename = data[1]
                send_data = "OK@"
                if filename in files:
                    os.remove(os.path.join(SERVER_DATA_PATH, filename))
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."
                conn.send(send_data.encode(FORMAT))

            elif cmd == "LOGOUT":
                break

            elif cmd == "HELP":
                help_text = (
                    "OK@"
                    "LIST: List all the files from the server.\n"
                    "UPLOAD <path>: Upload a file to the server.\n"
                    "DELETE <filename>: Delete a file from the server.\n"
                    "LOGOUT: Disconnect from the server.\n"
                    "HELP: List all the commands."
                )
                conn.send(help_text.encode(FORMAT))

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()

def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    main()
