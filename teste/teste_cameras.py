import cv2
import numpy as np

def todos_os_pix_iguais(frame):
    # Compara todos os pixels com o primeiro pixel
    return np.all(frame == frame[0, 0])

for i in range(10):
    cap = cv2.VideoCapture(i)

    if not cap.isOpened():
        print(f"❌ Câmera {i} não abriu.")
        continue

    ret, frame = cap.read()
    if not ret or frame is None or frame.size == 0:
        print(f"⚠️ Câmera {i} sem frame válido.")
    elif todos_os_pix_iguais(frame):
        cor = frame[0, 0]
        print(f"⚠️ Câmera {i} retornou uma imagem de cor única: {cor}")
        cv2.imshow(f'Câmera {i}', frame)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    else:
        print(f"✅ Câmera {i} está funcionando e tem imagem com conteúdo variado!")
        # Mostra o frame rapidamente
        cv2.imshow(f'Câmera {i}', frame)
        cv2.waitKey(500)
        cv2.destroyAllWindows()

    cap.release()
