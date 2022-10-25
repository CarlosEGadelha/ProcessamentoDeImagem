import cv2
import numpy as np
import matplotlib.pylab as plt

backroom = cv2.imread("imagens/backroom.jpg")
imagem = cv2.imread("imagens/backroom_cj.jpg")

##Converter para HSV
imagem_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

##Criar a mascara do laranja
##Vermelho (5, 75, 25)
##Laranja (25, 255, 255)
mascara = cv2.inRange(imagem_hsv, (30,0,0), (100,255,255))
imascara = mascara>0

cj = np.zeros_like(imagem, np.uint8)
cj[imascara] = imagem[imascara]

cj_verde = imagem.copy()
imagem_hsv[...,0] = imagem_hsv[...,0] + 20
cj_verde[imascara] = cv2.cvtColor(imagem_hsv, cv2.COLOR_HSV2BGR)[imascara]
cj_verde = np.clip(cj_verde, 0, 255)

backroom_cj = cv2.bitwise_and(backroom, backroom, mask=imascara.astype(np.uint8))
sem_cj = cv2.bitwise_and(imagem, imagem, mask=(np.bitwise_not(imascara).astype(np.uint8)))
sem_cj = sem_cj + backroom_cj

plt.figure(figsize=(20, 12))
plt.subplot(221), plt.imshow(cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB))
plt.subplot(222), plt.imshow(cv2.cvtColor(backroom, cv2.COLOR_BGR2RGB))
plt.subplot(223), plt.imshow(cv2.cvtColor(cj_verde, cv2.COLOR_BGR2RGB))
plt.subplot(224), plt.imshow(cv2.cvtColor(sem_cj, cv2.COLOR_BGR2RGB))
plt.show()

