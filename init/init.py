from ping3 import ping
import os
import logging
import time


def iniciar_logging():
    # Configurar o logging para escrever no arquivo "meu_log.log"
    logging.basicConfig(
        filename='./logs/application_logs.log',
        level=logging.DEBUG,              # Define o nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da mensagem
    )



def myping(host):
    resp = ping(host)

    return resp



def teste_rede():
    while (not myping("www.google.com")):
        logging.warning("Rede não está funcionando. Tentando novamente em 15 segundos")
        time.sleep(15)
    logging.info("Rede encontrada")

def teste_cameras():
    pass

def init():
    iniciar_logging()
    teste_rede()
    teste_cameras()