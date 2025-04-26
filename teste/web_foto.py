import cv2

# Inicializa a captura de vídeo (0 = webcam padrão)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: não foi possível acessar a webcam.")
    exit()

# Lê um único frame da webcam
ret, frame = cap.read()

if ret:
    # Salva a imagem capturada como 'foto.jpg'
    cv2.imwrite('foto.jpg', frame)
    print("Foto salva como 'foto.jpg'")
else:
    print("Erro: não foi possível capturar a imagem.")

# Libera a webcam
cap.release()
