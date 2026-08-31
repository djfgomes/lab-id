import socket

MULTICAST_GROUP = "239.1.1.1"
MULTICAST_PORT = 5007


def create_publisher_socket(interface_ip=None):
    """
    Cria um socket UDP configurado para enviar multicast.
    interface_ip: IP da interface de rede local por onde enviar
    (necessário quando há mais do que uma interface ativa, ex. Wi-Fi + Tailscale).
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = 1
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    if interface_ip:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF,
                         socket.inet_aton(interface_ip))

    return sock


def publish(sock, payload):
    sock.sendto(payload, (MULTICAST_GROUP, MULTICAST_PORT))