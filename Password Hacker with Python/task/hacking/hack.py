import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument("ip_adress", help="IP adress")
parser.add_argument("port", help="port")
parser.add_argument("message", help="message to send")

if __name__ == "__main__":
    args = parser.parse_args()

    with socket.socket() as client_socket:
        address = (args.ip_adress, int(args.port))
        client_socket.connect(address)
        client_socket.send(args.message.encode())
        response = client_socket.recv(1024)
        print(response.decode())