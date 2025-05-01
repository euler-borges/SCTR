import os
import logging
import time
import cv2
import threading
from datetime import datetime
from ultralytics import YOLO

lock_condition = threading.Lock()
cond_fill = threading.Condition(lock_condition)

target_class = 0 #classe alvo: pessoa
alert_threshold = 10  # Número de frames com detecção necessários para gerar alarme

alarm_buffer_count = 0  # Contador de alarmes
alarm_buffer = []  # Buffer para armazenar alarmes

def alarm_thread_func():
    global alarm_buffer_count, alarm_buffer
    while True:
        with cond_fill:
            while alarm_buffer_count == 0:
                cond_fill.wait()

            # Processa o buffer de alarmes
            while alarm_buffer_count > 0:
                alarm = alarm_buffer.pop(0)
                #teste 
                logging.info(f"Alarme: {alarm}")
                alarm_buffer_count -= 1

def camera_thread_func(camera_id, model):
    global alarm_buffer_count, alarm_buffer
    logging.info(f"Iniciando thread para câmera {camera_id}")
    alert_state = False
    frames_with_alert = 0

    cap = cv2.VideoCapture(camera_id)

    if not cap.isOpened():
        print(f"Erro ao abrir câmera {camera_id}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Falha na captura da câmera {camera_id}")
            break

        # Processa a imagem com YOLO
        results = model(frame, classes=[target_class])

        for result in results:
            if len(result.boxes) > 0:
                frames_with_alert += 1
                if frames_with_alert >= alert_threshold:
                    # Registra a detecção
                    frames_with_alert = 0
                    
                    with cond_fill:
                        alarm_buffer.append(f"{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}: Alerta na câmera {camera_id}.")
                        alarm_buffer_count += 1
                        cond_fill.notify()
                break  # registra uma vez por frame com detecção
            else:
                frames_with_alert = 0


    cap.release()
    cv2.destroyAllWindows()

def process(active_cameras):
    YOLO_MODELS = []
    for _ in active_cameras:
        YOLO_MODELS.append(YOLO("./YOLO_models/yolov8n.pt"))

    #inicia a thread de alarme
    logging.info("Iniciando thread de alarme")
    # Cria e inicia a thread de alarme
    thread_alarm = threading.Thread(target=alarm_thread_func)
    thread_alarm.start()

    threads_camera = []
    for i, camera_id in enumerate(active_cameras):
        thread = threading.Thread(target=camera_thread_func, args=(camera_id, YOLO_MODELS[i]))
        threads_camera.append(thread)
        thread.start()