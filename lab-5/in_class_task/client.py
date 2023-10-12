import socket
import threading
import json

SERVER = '127.0.0.1'
PORT = 8000

def listen_for_messages():
    while True:
        try:
            msg = client_sock.recv(1024).decode('utf-8')
            if not msg:
                print("Connection lost.")
                break

            msg_json = json.loads(msg)
            msg_type = msg_json.get('type')

            if msg_type == 'notification':
                print(msg_json['payload']['message'])
            elif msg_type == 'message':
                payload = msg_json['payload']
                print(f"{payload['sender']}: {payload['text']}")
            elif msg_type == 'connect_ack':
                print(msg_json['payload']['message'])
            else:
                print(f"Received: {msg_json}")

        except Exception as e:
            print(f"Error occurred: {e}")
            break

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_sock.connect((SERVER, PORT))

print(f"Connected to {SERVER}:{PORT}")

nickname = input("Enter nickname: ").strip()
while not nickname:
    print("Name cannot be empty.")
    nickname = input("Enter nickname: ").strip()

chat_room = input("Enter the room you want to join: ").strip()
while not chat_room:
    print("Room cannot be empty.")
    chat_room = input("Enter the room you want to join: ").strip()

connect_msg = {
    "type": "connect",
    "payload": {"name": nickname, "room": chat_room}
}

client_sock.send(json.dumps(connect_msg).encode('utf-8'))

receive_thread = threading.Thread(target=listen_for_messages)
receive_thread.daemon = True
receive_thread.start()

try:
    while True:
        text = input()
        if text.lower() == 'exit':
            break

        message = {
            "type": "message",
            "payload": {"sender": nickname, "room": chat_room, "text": text}
        }
        client_sock.send(json.dumps(message).encode('utf-8'))
except KeyboardInterrupt:
    print("Exiting the client.")
finally:
    client_sock.close()