import cv2

# Use 0 para a webcam padrão ou 1, 2... para outras. Teste com diferentes índices.
cap = cv2.VideoCapture(3)

if not cap.isOpened() or cap is None:
    print("Não foi possível acessar a câmera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Mostra a imagem
    cv2.imshow('Câmera do Celular', frame)

    # Sai com a tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
