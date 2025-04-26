from ultralytics import YOLO
import numpy as np
import cv2

# Carrega o modelo pré-treinado (YOLOv8n é o mais leve)
model = YOLO("yolo11n.pt")  # Você pode usar yolov8s.pt, yolov8m.pt, etc.

# Carrega a imagem tirada anteriormente
img_path = "foto.jpg"
results = model(img_path)

# Salva a imagem com as detecções
for result in results:
    result.save(filename="foto_processada.jpg")

print("Imagem processada salva como 'foto_processada.jpg'")
