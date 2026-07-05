import socket
import struct
import time
from generated.serializers import SensorPacket

HOST = '127.0.0.1'
PORT = 9999


def main():
    packet = SensorPacket(
        sender='sensor-01',
        receiver='receiver-01',
        value=23.7,
        unit='C'
    )
    payload = packet.serialize()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(struct.pack('<I', len(payload)) + payload)
        print('Sent sensor data:', packet.sender, '->', packet.receiver, packet.value, packet.unit)

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

        reply, _ = SensorPacket.deserialize(buf, 0)
        print('Receiver acknowledged:', reply.sender, '->', reply.receiver, reply.value, reply.unit)


if __name__ == '__main__':
    main()
