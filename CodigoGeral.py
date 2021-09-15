#Codigo Geral: Qualquer palavra / Qualquer um dos 4 numeros: '01', '02', '03', '04'
#Autor: Ramon Moratori 

#A imagem precisa ser em formato .jpg e de tamanho no maximo de 600x600
import tensorflow as tf
import pytesseract as pyt
import cv2
import os
from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import time
import serial


#__________________________________ARDUINO______________________________________________________
porta = "COM3" #DEFINA A PORTA USB CORRETA ONDE O ARDUINO ESTA LIGADO
velocidade = 9600
conexao = serial.Serial(porta, velocidade);
conexao.write(b'5') # Inicia enviando 5
valor_antigo = 5


#__________________________________IDENTIFICA O NUMERO__________________________________________

numeroencontrado = 0 
palavra = 0
encontrado = 0

strnumero = input('Digite o numero do produto a ser identificado com valor 0V (1,2,3, 4 ou 12): ')
strpalavra1 = input('Digite a palavra a ser identificada com valor 0V: ')
strpalavra2 = input('Digite uma variacao do nome a ser identificado: ')
strpalavra3 = input('Digite uma variacao do nome a ser identificado: ')
strpalavra1 = strpalavra1.upper()
strpalavra2 = strpalavra2.upper()
strpalavra3 = strpalavra3.upper()

#O modelo de aprendizado da Rede Neural e carregado (coloque-o na mesma pasta deste codigo)
model = load_model('keras_model.h5')

#E aberta a webcam e, de 1 em 1 segundo aproximadamente, o codigo salva o frame em uma imagem  
captura = cv2.VideoCapture(0)

while(1):
    t=time.time()
    ret, frame = captura.read()
    cv2.imshow("Video", frame)
   
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
    
    #Acessa o executavel do Tesseract no diretorio instalado do HD
    pyt.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe'
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    
    #Processa a imagem capturada pela camera
    size = (224, 224)
    image_array = cv2.resize(frame,size)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array

    #A Rede Neural faz a predicao do frame com base em seu treinamento
    prediction = model.predict(data)
    
    #Aqui aparece na tela a porcentagem de certeza das 4 categorias na analise do frame 
    print(prediction)
    
    #Aparece na tela a porcentagem de certeza do numero '02' (correspondente à categoria 01)
    print(prediction[0][1])

    #Aqui e transformada a certeza das categorias em valor alto para as variaveis que representam os numeros
    #A categoria que possui maior porcentagem de certeza, "vence" e um sinal alto vai para sua respectiva variavel
    if prediction[0][0] > prediction[0][1] and prediction[0][0] > prediction[0][2] and prediction[0][0] > prediction[0][3] and prediction[0][0] > prediction[0][4]  and prediction[0][0] > prediction[0][5]:
            print("Encontramos o numero '01'")
            numeroencontrado = '1'
            
    elif prediction[0][1] > prediction[0][0] and prediction[0][1] > prediction[0][2] and prediction[0][1] > prediction[0][3] and prediction[0][1] > prediction[0][4] and prediction[0][1] > prediction[0][5]:
            print("Encontramos o numero '02'")
            numeroencontrado = '2'
            
    elif prediction[0][2] > prediction[0][0] and prediction[0][2] > prediction[0][1] and prediction[0][2] > prediction[0][3] and prediction[0][2] > prediction[0][4] and prediction[0][2] > prediction[0][5]:
            print("Encontramos o numero '03'")
            numeroencontrado = '3'
            
    elif prediction[0][3] > prediction[0][0] and prediction[0][3] > prediction[0][1] and prediction[0][3] > prediction[0][2] and prediction[0][3] > prediction[0][4] and prediction[0][3] > prediction[0][5]:
            print("Encontramos o numero '04'")
            numeroencontrado = '4'
            
    elif prediction[0][4] > prediction[0][0] and prediction[0][4] > prediction[0][1] and prediction[0][4] > prediction[0][2] and prediction[0][4] > prediction[0][3] and prediction[0][4] > prediction[0][5]:
            print("Nenhum numero encontrado")
            numeroencontrado = '0'
    
    elif prediction[0][5] > prediction[0][0] and prediction[0][5] > prediction[0][1] and prediction[0][5] > prediction[0][2] and prediction[0][5] > prediction[0][3] and prediction[0][5] > prediction[0][4]:
            print("Encontramos o numero 12")
            numeroencontrado = '12'
            
#_________________________MASCULINO OU FEMININO______________________________________
    
    palavra = 0
    if strnumero == numeroencontrado or strnumero == '0'+numeroencontrado:
        abrir = Image.fromarray(frame)
        texto = pyt.image_to_string(abrir).upper()
        
        print("Texto Encontrado na Imagem: " + texto)
    
        #Considera as tres variacoes que a palavra pode ter e usa o Tesseract para analisar se elas estao contidas na imagem
        if strpalavra1 in texto or strpalavra2 in texto or strpalavra3 in texto:
          print("Encontramos a palavra" + strpalavra1)
          
          #Encontrou a palavra: palavra = 1 pois foi encontrada na imagem
          palavra = 1
      
    
    #___________________________________SINAL PARA O RASPBERRY____________________________________
    
    if palavra and valor_antigo == 5:
        conexao.write(b'0')#Inverter o valor de 5 ou 0
        valor_antigo = 0
        print('Foi encontra')
    elif valor_antigo == 0:
        conexao.write(b'5')#Inverter o valor de 5 ou 0
        valor_antigo = 5
    
#Fecha a webcam ao apertar 'ESC'
conexao.close()      
captura.release()
cv2.destroyAllWindows()
