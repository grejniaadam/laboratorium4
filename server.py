import socket
import struct
from generated.serializers import Message, Person, SensorPacket

HOST = '127.0.0.1'
PORT = 9999


def handle_conn(conn):
    data = conn.recv(4)
    if len(data) < 4:
        return

    size = struct.unpack('<I', data)[0]
    buf = b''
    while len(buf) < size:
        chunk = conn.recv(size - len(buf))
        if not chunk:
            break
        buf += chunk

    try:
        msg, _ = Message.deserialize(buf, 0)
        print('Server received message:', msg.sender.name, msg.sender.age, msg.text)
        reply = Message(sender=msg.sender, text='ACK: ' + msg.text)
    except Exception:
        packet, _ = SensorPacket.deserialize(buf, 0)
        print('Server received sensor packet:', packet.sender, packet.receiver, packet.value, packet.unit)
        reply = SensorPacket(sender=packet.receiver, receiver=packet.sender, value=packet.value, unit=packet.unit)

    payload = reply.serialize()
    conn.sendall(struct.pack('<I', len(payload)) + payload)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print('Server listening on', HOST, PORT)
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                handle_conn(conn)


if __name__ == '__main__':
    main()
