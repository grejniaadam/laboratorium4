import socket
from generated.serializers import Message, Person

HOST = '127.0.0.1'
PORT = 9999

def handle_conn(conn):
    # receive size-prefixed message (uint32 length)
    data = conn.recv(4)
    if len(data) < 4:
        return
    import struct
    size = struct.unpack('<I', data)[0]
    buf = b''
    while len(buf) < size:
        chunk = conn.recv(size - len(buf))
        if not chunk:
            break
        buf += chunk
    msg, _ = Message.deserialize(buf, 0)
    print('Server received:', msg.sender.name, msg.sender.age, msg.text)

    # modify and send back
    reply = Message(sender=msg.sender, text='ACK: ' + msg.text)
    payload = reply.serialize()
    conn.sendall(struct.pack('<I', len(payload)) + payload)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        print('Server listening on', HOST, PORT)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            handle_conn(conn)

if __name__ == '__main__':
    main()
