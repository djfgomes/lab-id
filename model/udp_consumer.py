import socket
import struct
import json

MULTICAST_GROUP = "239.1.1.1"
MULTICAST_PORT = 5007


def create_subscriber_socket():
    """Cria um socket UDP e subscreve o grupo multicast."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind(("", MULTICAST_PORT))

    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack("4sL", group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


if __name__ == "__main__":
    sock = create_subscriber_socket()
    print(f"À escuta em {MULTICAST_GROUP}:{MULTICAST_PORT}...")

    while True:
        data, addr = sock.recvfrom(4096)
        message = json.loads(data.decode("utf-8"))
        print(f"Frame {message['frame_id']}: {len(message['detections'])} deteções")