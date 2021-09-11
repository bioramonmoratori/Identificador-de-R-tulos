#Codigo Geral: Qualquer palavra / Qualquer um dos 4 números: '01', '02', '03', '04'
#Autor: Ramon Moratori 

#A imagem precisa ser em formato .jpg e de tamanho no mÃ¡ximo de 600x600

import pytesseract as pyt
import cv2
import os
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import time
import serial


#__________________________________ARDUINO______________________________________________________
porta = "COM3" #DEFINA A PORTA USB CORRETA ONDE O ARDUINO ESTA LIGADO
velocidade = 9600
conexao = serial.Serial(porta, velocidade);

#__________________________________IDENTIFICA O NUMERO__________________________________________

numeroencontrado = 0 
palavra = 0
encontrado = 0

strnumero = input('Digite o número do produto a ser identificado com valor 0V (1,2,3 ou 4): ')
strpalavra1 = input('Digite a palavra a ser identificada com valor 0V: ')
strpalavra2 = input('Digite uma variação do nome a ser identificado: ')
strpalavra3 = input('Digite uma variação do nome a ser identificado: ')



#O modelo de aprendizado da Rede Neural é carregado (coloque-o na mesma pasta deste código)
model = load_model('keras_model.h5')

#É aberta a webcam e, de 1 em 1 segundo aproximadamente, o código salva o frame em uma imagem  
captura = cv2.VideoCapture(0)

while(1):
    ret, frame = captura.read()
    cv2.imshow("Video", frame)
   
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    
    #Salva o frame da câmera na mesma pasta em que este código está
    cv2.imwrite('./camera.jpg', frame)
    
    #Acessa o executável do Tesseract no diretório instalado do HD
    pyt.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    

    #ATENÇÃO: a imagem que é identificada pela rede neural não pode ter um tamanho muito grande e precisa ser .jpg
    image = Image.open('./camera.jpg')
    
    #Processa a imagem capturada pela câmera
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    #A Rede Neural faz a predição do frame com base em seu treinamento
    prediction = model.predict(data)
    
    #Aqui aparece na tela a porcentagem de certeza das 4 categorias na análise do frame 
    print(prediction)
    
    #Aparece na tela a porcentagem de certeza do número '02' (correspondente à categoria 01)
    print(prediction[0][1])

    #Aqui é transformada a certeza das categorias em valor alto para as variáveis que representam os números
    #A categoria que possui maior porcentagem de certeza, "vence" e um sinal alto vai para sua respectiva variável
    if prediction[0][0] > prediction[0][1] and prediction[0][0] > prediction[0][2] and prediction[0][0] > prediction[0][3] and prediction[0][0] > prediction[0][4]:
            print("Encontramos o numero '01'")
            numeroencontrado = '1'
            
            time.sleep(0.1)
            
    elif prediction[0][1] > prediction[0][0] and prediction[0][1] > prediction[0][2] and prediction[0][1] > prediction[0][3] and prediction[0][1] > prediction[0][4]:
            print("Encontramos o numero '02'")
            numeroencontrado = '2'
            
            time.sleep(0.1)
            
    elif prediction[0][2] > prediction[0][0] and prediction[0][2] > prediction[0][1] and prediction[0][2] > prediction[0][3] and prediction[0][2] > prediction[0][4]:
            print("Encontramos o numero '03'")
            numeroencontrado = '3'
            
            time.sleep(0.1)
            
    elif prediction[0][3] > prediction[0][0] and prediction[0][3] > prediction[0][1] and prediction[0][3] > prediction[0][2] and prediction[0][3] > prediction[0][4]:
            print("Encontramos o numero '04'")
            numeroencontrado = '4'
            
            time.sleep(0.1)
            
    elif prediction[0][4] > prediction[0][0] and prediction[0][4] > prediction[0][1] and prediction[0][4] > prediction[0][2] and prediction[0][4] > prediction[0][3]:
            print("Nenhum numero encontrado")
            numeroencontrado = '0'
            
            time.sleep(0.1)
    
#_________________________MASCULINO OU FEMININO______________________________________

    

    #Abrimos novamente o frame (lembrando que ele segue as mesmas regras ditas anteriormente)
    imagem = cv2.imread("./camera.jpg", 1)  
    
    #São declaradas, com sinal baixo, as varíaveis que representam a identificação das palavras possíveis
    #A variável 'encontrado' existe em casos dele não encontrar nenhuma palavra

    
    #salva a imagem em um arquivo temporário do Windows para aplicar OCR
    filenameImagem = "{}.png".format(os.getpid())
    cv2.imwrite(filenameImagem, imagem)
    
    #carrega a imagem usando a biblioteca PIL/Pillow e aplica OCR
    texto = pyt.image_to_string(Image.open(filenameImagem))

    #deleta arquivo temporário
    os.remove(filenameImagem)
    
    #A palavra extraída da imagem é salva na variável 'texto'


    #Printa o texto todo que aparece na imagem
    print("Texto Encontrado na Imagem: " + texto)

    #Considera as três variações que a palavra pode ter e usa o Tesseract para analisar se elas estão contidas na imagem
    if strpalavra1 in texto or strpalavra2 in texto or strpalavra3 in texto:
      print("Encontramos a palavra" + strpalavra1)
      
      #Encontrou a palavra: palavra = 1 pois foi encontrada na imagem
      palavra = 1
      encontrado = 1

     
    #Se ele não encontra nenhuma palavra    
    if encontrado == 0: 
      print("Não encontramos " + strpalavra1)
      palavra = 0
      
    

    #redimensiona só pra ser exibido ao final
    imagem = cv2.resize(imagem,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)

    
    #___________________________________SINAL PARA O RASPBERRY____________________________________
    
    #Caso encontre o produto todo (número e palavra)
    if strnumero in numeroencontrado and palavra == 1:
      print("Resultado: Detectamos o produto " + strnumero + strpalavra1)
      
      #Envia um sinal baixo em uma das portas do Raspberry PI (5V) / Não faz nada
      conexao.write(b'5')
      time.sleep(3)

    
    #Caso encontre qualquer coisa diferente do produto mencionado
    else:
      print("Resultado: Não foi encontrado o produto " + strnumero + strpalavra1)
      
      #Envia um sinal alto em uma das portas do Raspberry PI (0V) 
      conexao.write(b'0')
      #time.sleep(0.5)
    
    palavra = 0
    numeroencontrado = '0'
    
#Fecha a webcam ao apertar 'ESC'
conexao.close()      
captura.release()
cv2.destroyAllWindows()
