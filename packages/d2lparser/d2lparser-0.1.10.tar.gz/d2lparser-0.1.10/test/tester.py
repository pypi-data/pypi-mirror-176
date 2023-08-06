
import socket


def main():

    host = socket.gethostname()
    port = 7845
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(bytes.fromhex("0300300045c9612505000000010000004df3d038ebaa7067e4273fa2c44a1beaba5515a63a04d228da47ceb0e37a6286"))

main()
