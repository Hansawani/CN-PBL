import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 4456
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        cmd, msg = data.split("@", 1)

        if cmd == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        elif cmd == "OK":
            print(f"{msg}")

        data = input("> ")
        data = data.strip().split(" ")
        cmd = data[0].upper()

        if cmd == "HELP":
            client.send(cmd.encode(FORMAT))

        elif cmd == "LOGOUT":
            client.send(cmd.encode(FORMAT))
            break

        elif cmd == "LIST":
            client.send(cmd.encode(FORMAT))

        elif cmd == "DELETE":
            if len(data) < 2:
                print("[ERROR] Usage: DELETE <filename>")
                continue
            client.send(f"{cmd}@{data[1]}".encode(FORMAT))

        elif cmd == "UPLOAD":
            if len(data) < 2:
                print("[ERROR] Usage: UPLOAD <file_path>")
                continue
            path = data[1]
            try:
                with open(path, "r") as f:
                    text = f.read()
                filename = path.split("/")[-1]
                send_data = f"{cmd}@{filename}@{text}"
                client.send(send_data.encode(FORMAT))
            except FileNotFoundError:
                print("[ERROR] File not found.")

    print("Disconnected from the server.")
    client.close()

if __name__ == "__main__":
    main()
