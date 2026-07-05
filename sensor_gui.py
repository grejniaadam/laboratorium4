import struct
import socket
from generated.serializers import SensorPacket

HOST = '127.0.0.1'
PORT = 9999


def send_sensor_packet(sender, receiver, value, unit):
    packet = SensorPacket(sender=sender, receiver=receiver, value=float(value), unit=unit)
    payload = packet.serialize()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(struct.pack('<I', len(payload)) + payload)

            data = s.recv(4)
            if len(data) < 4:
                return None
            size = struct.unpack('<I', data)[0]
            buf = b''
            while len(buf) < size:
                chunk = s.recv(size - len(buf))
                if not chunk:
                    break
                buf += chunk

            reply, _ = SensorPacket.deserialize(buf, 0)
            return reply
    except ConnectionRefusedError:
        return None


if __name__ == '__main__':
    reply = send_sensor_packet('sensor-gui', 'receiver-gui', 21.3, 'C')
    print(reply.sender, reply.receiver, reply.value, reply.unit)
