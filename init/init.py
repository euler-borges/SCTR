import socket
from ping3 import ping
import os




def myping(host):
    resp = ping(host)

    if resp == False:
        return False
    else:
        return True


print(myping("www.google.com"))

def teste_rede():

    def ping(host):
        response = os.system("ping -c 1 " + host)
        return response == 0

    def get_ip():
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    print("Teste de rede")
    print("IP:", get_ip())
    print("Ping google.com:", ping("google.com"))

def teste_cameras():


def init():
    teste_rede()
    teste_cameras()