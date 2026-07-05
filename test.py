#!/usr/bin/env python
"""
Integration test: starts server, runs client, verifies communication.
"""
import subprocess
import time
import socket
import sys
import threading
from generated.serializers import Message, Person, Product, Order
from sensor_gui import send_sensor_packet

def test_person_serialization():
    """Test Person serialization/deserialization."""
    p = Person(id=42, name="TestUser", age=25)
    data = p.serialize()
    p2, _ = Person.deserialize(data, 0)
    assert p2.id == 42
    assert p2.name == "TestUser"
    assert p2.age == 25
    print("✓ Person serialization test passed")

def test_product_serialization():
    """Test Product serialization/deserialization."""
    prod = Product(sku=9999, title="Widget", price=49.99)
    data = prod.serialize()
    prod2, _ = Product.deserialize(data, 0)
    assert prod2.sku == 9999
    assert prod2.title == "Widget"
    assert prod2.price == 49.99
    print("✓ Product serialization test passed")

def test_order_serialization():
    """Test Order with nested Product."""
    prod = Product(sku=12345, title="Laptop", price=999.99)
    order = Order(order_id=1, product=prod, quantity=2, notes="Urgent")
    data = order.serialize()
    order2, _ = Order.deserialize(data, 0)
    assert order2.order_id == 1
    assert order2.product.sku == 12345
    assert order2.product.title == "Laptop"
    assert order2.product.price == 999.99
    assert order2.quantity == 2
    assert order2.notes == "Urgent"
    print("✓ Order serialization test passed")

def test_message_serialization():
    """Test Message with nested Person."""
    p = Person(id=1, name="Alice", age=30)
    msg = Message(sender=p, text="Hello World")
    data = msg.serialize()
    msg2, _ = Message.deserialize(data, 0)
    assert msg2.sender.id == 1
    assert msg2.sender.name == "Alice"
    assert msg2.sender.age == 30
    assert msg2.text == "Hello World"
    print("✓ Message serialization test passed")

def test_server_stays_alive_for_multiple_connections():
    """Test that the server keeps accepting new connections after the first one."""
    server_proc = subprocess.Popen([sys.executable, "server.py"])
    time.sleep(1)
    try:
        payload = Message(sender=Person(id=7, name="Alice", age=27), text="First ping").serialize()
        with socket.create_connection(("127.0.0.1", 9999), timeout=1) as s:
            s.sendall(struct.pack('<I', len(payload)) + payload)
            data = s.recv(4)
            assert len(data) == 4

        payload = Message(sender=Person(id=8, name="Bob", age=31), text="Second ping").serialize()
        with socket.create_connection(("127.0.0.1", 9999), timeout=1) as s:
            s.sendall(struct.pack('<I', len(payload)) + payload)
            data = s.recv(4)
            assert len(data) == 4
    finally:
        server_proc.terminate()
        server_proc.wait()


def test_tcp_communication():
    """Test TCP server/client communication."""
    import struct
    
    # Start server in background
    server_proc = subprocess.Popen([sys.executable, "server.py"])
    time.sleep(1)  # Give server time to start
    
    try:
        # Create and send message
        p = Person(id=100, name="TestClient", age=40)
        msg = Message(sender=p, text="Test message from client")
        payload = msg.serialize()
        
        # Connect and communicate
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 9999))
            s.sendall(struct.pack('<I', len(payload)) + payload)
            
            # Receive reply
            data = s.recv(4)
            if len(data) < 4:
                raise RuntimeError("Failed to receive reply size")
            size = struct.unpack('<I', data)[0]
            buf = b''
            while len(buf) < size:
                chunk = s.recv(size - len(buf))
                if not chunk:
                    break
                buf += chunk
            
            reply, _ = Message.deserialize(buf, 0)
            assert reply.text.startswith("ACK:")
            assert "Test message from client" in reply.text
            print("✓ TCP communication test passed")
    finally:
        # Kill server
        server_proc.terminate()
        server_proc.wait()


def test_sensor_gui_send():
    """Test sending a SensorPacket via GUI helper."""
    server_proc = subprocess.Popen([sys.executable, "server.py"])
    time.sleep(1)
    try:
        reply = send_sensor_packet('sensor-gui', 'receiver-gui', 88.8, 'C')
        assert reply is not None
        assert reply.sender == 'receiver-gui'
        assert reply.receiver == 'sensor-gui'
        print("✓ Sensor GUI send test passed")
    finally:
        server_proc.terminate()
        server_proc.wait()

if __name__ == "__main__":
    print("Running integration tests...\n")
    try:
        test_person_serialization()
        test_product_serialization()
        test_order_serialization()
        test_message_serialization()
        test_tcp_communication()
        test_sensor_gui_send()
        print("\n✓ All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
