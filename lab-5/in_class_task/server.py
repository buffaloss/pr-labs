import socket
import threading
import json

SERVER = '127.0.0.1'
PORT = 8000

active_clients = []
chat_rooms = {}

def message_format(msg_type, content):
    return json.dumps({"type": msg_type, "payload": content})

def client_handler(client_sock, client_addr):
    global active_clients, chat_rooms
    client_id = ""
    client_chat_room = ""

    while True:
        try:
            received_message = client_sock.recv(1024).decode('utf-8')
            if not received_message:
                break

            message_info = json.loads(received_message)
            print(f"Received: {received_message}")

            if message_info["type"] == "connect":
                client_id = message_info["payload"]["name"]
                client_chat_room = message_info["payload"]["room"]
                room_clients = chat_rooms.get(client_chat_room, [])
                room_clients.append(client_sock)
                chat_rooms[client_chat_room] = room_clients

                ack_msg = message_format("connect_ack", {"message": "Connected to the room."})
                client_sock.send(ack_msg.encode('utf-8'))
                print(f"{client_id} connected to room {client_chat_room}")

                notify_msg = message_format("notification", {"message": f"{client_id} has joined the room."})
                for client in room_clients:
                    if client != client_sock:
                        client.send(notify_msg.encode('utf-8'))

            elif message_info["type"] == "message":
                room_clients = chat_rooms.get(client_chat_room, [])
                broadcast_msg = message_format("message", {
                    "sender": client_id,
                    "room": client_chat_room,
                    "text": message_info["payload"]["text"]
                })
                print(f"Message in {client_chat_room} from {client_id}: {message_info['payload']['text']}")
                for client in room_clients:
                    client.send(broadcast_msg.encode('utf-8'))

        except json.JSONDecodeError:
            print(f"Received invalid JSON data from {client_addr}. Continuing...")

    active_clients.remove(client_sock)
    if client_chat_room in chat_rooms:
        chat_rooms[client_chat_room].remove(client_sock)
    client_sock.close()
    print(f"Connection from {client_addr} closed.")

if __name__ == "__main__":
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((SERVER, PORT))
    server_sock.listen()
    print(f"Server is listening on {SERVER}:{PORT}")

    try:
        while True:
            client_sock, client_addr = server_sock.accept()
            active_clients.append(client_sock)
            client_thread = threading.Thread(target=client_handler, args=(client_sock, client_addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Shutting down the server.")
    finally:
        server_sock.close()