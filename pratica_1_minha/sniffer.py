import ipaddress
import sys
from concurrent.futures import ThreadPoolExecutor
from ping3 import ping, verbose_ping
import threading

# Definindo o número máximo de threads
MAX_THREADS = 128

arquivo_resultados = "resultado.txt"


def ping_host(ip):
    try:
        response = ping(str(ip), timeout=1)
        if response:
            print(f"[+] {ip} está ativo")
            escreve_resultado(f"[+] {ip} está ativo")

    except PermissionError:
        print("⚠️ Permissão negada para enviar pacotes ICMP. Execute com sudo/admin.")
        sys.exit(1)
    except Exception as e:
        print(f"[+] {ip} está inativo")  # Ignora erros de timeout ou host unreachable
        escreve_resultado(f"[+] {ip} está inativo")

def startup():
    if len(sys.argv) != 3:
        print("Uso: python scanner.py <IP/MASCARA> modo")
        print("Exemplo: python scanner.py 192.168.0.0/24 1")
        sys.exit(1)

    if sys.argv[2] not in ["single", "fixed", "dinamic"]:
        print("Modo inválido. Use 'single', 'fixed' ou 'dynamic'.")
        sys.exit(1)

    with open(arquivo_resultados, "w") as f:
        f.write("Resultados do Scanner:\n")
        f.write("========================================\n")

def escreve_resultado(string):
    with open(arquivo_resultados, "a") as f:
        f.write(string + "\n")

    print(string)

def scanner():
    rede = sys.argv[1]
    modo = sys.argv[2]


    try:
        network = ipaddress.ip_network(rede, strict=False)
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)

    print(f"🔍 Escaneando rede: {network}...\n")
    hosts = network.hosts()
    print(hosts)

    if modo == "single":
        for ip in network.hosts():
            ping_host(ip)
    elif modo == "fixed":

        for ip in network.hosts():
            ping_host(ip)
    
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        for ip in network.hosts():
            executor.submit(ping_host, ip)

def main():
    startup()
    scanner()

if __name__ == "__main__":
    main()
