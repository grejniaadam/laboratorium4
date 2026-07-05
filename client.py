import socket
from generated.serializers import Message, Person

HOST = '127.0.0.1'
PORT = 9999

def main():
    p = Person(id=42, name='Alice', age=30)
    msg = Message(sender=p, text='Hello server')
    payload = msg.serialize()

    import struct
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(struct.pack('<I', len(payload)) + payload)

        data = s.recv(4)
        if len(data) < 4:
            return
        size = struct.unpack('<I', data)[0]
        buf = b''
        while len(buf) < size:
            chunk = s.recv(size - len(buf))
            if not chunk:
                break
            buf += chunk
        reply, _ = Message.deserialize(buf, 0)
        print('Client received reply:', reply.text)

if __name__ == '__main__':
    main()
