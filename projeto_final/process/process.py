import os
import logging
import time
import cv2
import threading
import requests.exceptions

from datetime import datetime
from ultralytics import YOLO
from twilio.rest import Client

from my_secrets.my_secrets import twilio_number, my_number

#definindo os locks e conditionals necessários para o funcionamento do sistema
lock_condition_alarm_buffer = threading.Lock()
cond_fill_alarm_buffer = threading.Condition(lock_condition_alarm_buffer)
lock_condition_sent_buffer = threading.Lock()
cond_fill_sent_buffer = threading.Condition(lock_condition_sent_buffer)

stop_event = threading.Event()

# Variaveis globais para o processamento de imagens
target_class = 0 #classe alvo: pessoa
alert_threshold = 10  # Número de frames com detecção necessários para gerar alarme

# Variaveis para armazzenar alarmes e permitir comunicação entre as threads
# alarm_buffer_count = 0  # Contador de alarmes
alarm_buffer = []  # Buffer para armazenar alarmes
sent_buffer = []  # Buffer para armazenar mensagens enviados

def send_sms_twilio(client, text_message):
    global sent_buffer
    global alarm_buffer
    try:
        message = client.messages.create(
            body=text_message,
            from_=twilio_number,
            to=my_number,
        )
        
        # Adiciona a mensagem ao buffer de mensagens enviadas
        with cond_fill_sent_buffer:
            sent_buffer.append((message, text_message))
            # Notifica a thread de confirmação de mensagens enviadas
            cond_fill_sent_buffer.notify()
            logging.info(f"Mensagem enviada para servidor Twilio: {message.sid}")
        return True  # Retorna True se a mensagem foi enviada com sucesso
    
    #para caso de erro no envio da mensagem
    except Exception as e:
        with cond_fill_alarm_buffer:
            alarm_buffer.append(text_message)

        logging.error(f"Erro ao enviar SMS: {e}")
        time.sleep(5)  # Espera 5 segundos antes de tentar novamente
        return False


def alarm_thread_func(twilio_client):
    # global alarm_buffer_count, alarm_buffer
    global alarm_buffer


    while not stop_event.is_set():
        with cond_fill_alarm_buffer:
            while not alarm_buffer:
                cond_fill_alarm_buffer.wait()

            local_buffer = alarm_buffer[:]
            alarm_buffer.clear()

            # Processa o buffer de alarmes
        
        for alarm_message in local_buffer:
            send_sms_twilio(twilio_client, alarm_message)


def confirm_sent_thread_func(twilio_client):
    global sent_buffer
    while not stop_event.is_set():
        with cond_fill_sent_buffer:
            while not sent_buffer and not stop_event.is_set():
                cond_fill_sent_buffer.wait()
            local_sent = sent_buffer[:]
            sent_buffer.clear()

            # Processa o buffer de mensagens enviadas
        for message, text_message in local_sent:
            # Verifica o status da mensagem
        
            while message.status not in ["undelivered", "delivered", "failed"] and not stop_event.is_set():
                try:
                    message = twilio_client.messages(message.sid).fetch()
                except Exception as e:
                    logging.error(f"Erro ao verificar status da mensagem: {e}")
                
                time.sleep(5)

            if message.status == "undelivered" or message.status == "failed":
                logging.info(f"Mensagem não entregue: {message.sid}")
                with cond_fill_alarm_buffer:
                    alarm_buffer.append(text_message)
                    cond_fill_alarm_buffer.notify()
            else:
                logging.info(f"Mensagem entregue: {message.sid}")
            
 
def camera_thread_func(camera_id, model):
    global alarm_buffer
    logging.info(f"Iniciando thread para câmera {camera_id}")
    frames_with_alert = 0

    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        logging.error(f"Erro ao abrir câmera {camera_id}")
        return

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            logging.error(f"Falha na captura da câmera {camera_id}")
            break

        # Processa a imagem com YOLO
        results = model(frame, classes=[target_class])

        for result in results:
            if len(result.boxes) > 0:
                frames_with_alert += 1
                if frames_with_alert >= alert_threshold:
                    # Registra a detecção
                    frames_with_alert = 0
                    
                    with cond_fill_alarm_buffer:
                        alarm_buffer.append(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}: Alerta na câmera {camera_id}.")
                        logging.info(f"Alerta na câmera {camera_id}.")
                        cond_fill_alarm_buffer.notify()
                    
                    time.sleep(30)  # Espera um pouco para evitar múltiplos alarmes
                break  # registra uma vez por frame com detecção
            else:
                frames_with_alert = 0


    cap.release()
    cv2.destroyAllWindows()

def process(twilio_client, active_cameras):
    YOLO_MODELS = []
    for _ in active_cameras:
        YOLO_MODELS.append(YOLO("./YOLO_models/yolov8n.pt"))

    #inicia a thread de alarme
    logging.info("Iniciando thread de alarme")
    # Cria e inicia a thread de alarme
    thread_alarm = threading.Thread(target=alarm_thread_func, args=(twilio_client,))
    thread_alarm.start()

    #inicia a thread de confirmação de mensagens enviadas
    logging.info("Iniciando thread de confirmação de mensagens enviadas")
    # Cria e inicia a thread de confirmacao de mensagens enviadas
    thread_confirm = threading.Thread(target=confirm_sent_thread_func, args=(twilio_client,))
    thread_confirm.start()

    #inicia as threads de camera
    threads_camera = []
    for i, camera_id in enumerate(active_cameras):
        thread = threading.Thread(target=camera_thread_func, args=(camera_id, YOLO_MODELS[i]))
        threads_camera.append(thread)
        thread.start()


    try:
        while True:
            time.sleep(1)  # mantém a thread principal viva
    except KeyboardInterrupt:
        logging.info("Encerrando sistema...")

        stop_event.set()

        with cond_fill_alarm_buffer:
            cond_fill_alarm_buffer.notify_all()
        with cond_fill_sent_buffer:
            cond_fill_sent_buffer.notify_all()

        thread_alarm.join()
        thread_confirm.join()
        for t in threads_camera:
            t.join()

        logging.info("Sistema encerrado com segurança.")