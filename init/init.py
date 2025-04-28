from ping3 import ping
import os
import logging
import time
import cv2
import numpy as np


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
    return teste_cameras()
