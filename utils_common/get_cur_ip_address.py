import socket


def get_cur_local_ip() -> str:
    hostname = socket.gethostname()
    current_local_ip = socket.gethostbyname(hostname)
    print(f"Current local IP address: {current_local_ip}")
    return current_local_ip
