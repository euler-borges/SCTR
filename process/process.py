import os
import logging
import time
import cv2
import threading
from ultralytics import YOLO

target_class = 0 #classe alvo: pessoa

def camera_thread(camera_id, model):
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

        # Mostra a imagem (opcional)
        annotated_frame = results[0].plot()
        cv2.imshow(f"Câmera {camera_id}", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def process(active_cameras):
    YOLO_MODELS = []
    for i in range(active_cameras):
        YOLO_MODELS.append(YOLO("./YOLO_models/yolov8n.pt"))