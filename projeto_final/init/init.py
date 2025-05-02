from ping3 import ping
import os
import logging
import time
import cv2
import numpy as np
from twilio.rest import Client
from my_secrets.my_secrets import account_sid, auth_token, twilio_number, my_number

def iniciar_logging():
    # Configurar o logging para escrever no arquivo "./logs/application_logs.log"
    logging.basicConfig(
        filename='./logs/application_logs.log',
        level=logging.DEBUG,              # Define o nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(levelname)s - %(message)s'  # Formato da mensagem
    )


def teste_rede():
    while (not ping("www.google.com")):
        logging.warning("Rede não está funcionando. Tentando novamente em 15 segundos")
        time.sleep(15)
    logging.info("Rede encontrada")


def iniciar_twilio():
    while True:
        # Verifica se o Twilio está funcionando
        try:
            client = Client(account_sid, auth_token)
            logging.info("Twilio iniciado com sucesso")
            return client
        except Exception as e:
            logging.error(f"Erro ao iniciar Twilio: {e}")
            time.sleep(15)


def teste_cameras():
    active_cameras = []
    logging.info("Iniciando teste de câmeras")
    while active_cameras == []:
        def todos_os_pix_iguais(frame):
            # Compara todos os pixels com o primeiro pixel
            return np.all(frame == frame[0, 0])

        for i in range(10):
            cap = cv2.VideoCapture(i)

            if cap.isOpened():
                logging.info(f"Câmera {i} encontrada aberta.")
            
                ret, frame = cap.read()
                if not ret or frame is None or frame.size == 0:
                    logging.error(f"Câmera {i} sem frame válido.")
                elif todos_os_pix_iguais(frame):
                    cor = frame[0, 0]
                    logging.error(f"Câmera {i} retornou uma imagem de cor única: {cor}")
                else:
                    logging.info(f"Câmera {i} está funcionando e tem imagem com conteúdo variado")
                    active_cameras.append(i)
            else:
                logging.warning(f"Câmera {i} não abriu.")

            cap.release()

    return active_cameras

def init():
    iniciar_logging()
    teste_rede()
    client = iniciar_twilio()
    active_cameras = teste_cameras()
    return (client, active_cameras)
