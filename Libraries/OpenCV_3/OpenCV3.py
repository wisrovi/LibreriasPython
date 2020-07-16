import numpy as np
import time
import cv2
import os.path as path

class OpenCV_3():
    """
    Esta es una manera que no utiliza el tradicional Haar de OpenCV, pues al ser basados en FaceRest es algo lento
    y aumentar la velocidad del reconocimiento es posible con el LBP de OpenCV, se pierde presición
    para ello, se presenta un modelo de DeepLearning que usa los algoritmos de FaceNet de google
    para buscar los rostros de manera optima y rapida
    """    

    """
        - El detector facial de aprendizaje profundo de OpenCV se basa en el marco del Detector de disparo único (SSD) con una red base ResNet
        - aplicar la detección de rostros con OpenCV a imágenes de entrada única.
        - El detector de rostro OpenCV más preciso se basa en el aprendizaje profundo y, en particular, utiliza el marco del Detector de disparo único (SSD) con ResNet como la red base.
        - Gracias al arduo trabajo de Aleksandr Rybnikov y los demás colaboradores de OpenCV dnn  módulo, podemos disfrutar de estos detectores faciales OpenCV más precisos en nuestras propias aplicaciones.
    """
    # https://github.com/opencv/opencv/tree/master/samples/dnn/face_detector
    def __init__(self, confianza=0.55):
        BASE_DIR = path.dirname(path.realpath(__file__))
        protocolo = BASE_DIR + "/" + "deploy.prototxt.txt" # arquitectura del modelo
        model = BASE_DIR + "/" + "res10_300x300_ssd_iter_140000.caffemodel" # pesos
        print()
        if not path.exists(model):
            self.failed = True
            print("No se encuetra el archivo model")
        elif not path.exists(protocolo):
            self.failed = True
            print("No se encuetra el archivo protocolo")
        else:
            self.failed = False
            self.net = cv2.dnn.readNetFromCaffe(protocolo, model)
        self.confianza = confianza
        
    def setConfianzaDeteccion(self, confianza):
        self.confianza = confianza
    
    def detectarRostros(self, imagen):
        listadoCoordenadasRostro = list()
        if self.failed == False:
            (h, w) = imagen.shape[:2]
            # la imagen generalmente viene en formato BGR pero la RNa usa RGB, blobFromImage hara la inversión de canales por nosotros
            # En caso de ser una sola imagen se usa: blobFromImage, pero si fueran muchas imagenes se usa: blobFromImages
            blob = cv2.dnn.blobFromImage(
                    image=cv2.resize(imagen, (300, 300)), # rescalamos el rostro al dimen int de la RNA
                    scalefactor=1.0, # normalizamos la imagen
                    size=(300, 300),
                    mean=(104.0, 177.0, 123.0) # le entregamos la resta media (R, G, B) con la que se entrenó la RNa para acoplar los colores del face esta media
                ) # blob = nuestra imagen de entrada después de la resta media, la normalización y el intercambio de canales.
            self.net.setInput(blob)
            self.detections = self.net.forward()            
            for i in range(0, self.detections.shape[2]):
                confianzaEsteRostro = self.detections[0, 0, i, 2]
                if confianzaEsteRostro >= self.confianza:
                    # Si la confianza alcanza el umbral mínimo
                    box = self.detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    coordenadas = (startX, startY, endX, endY, confianzaEsteRostro)
                    listadoCoordenadasRostro.append(coordenadas)
                
        return listadoCoordenadasRostro

    def PintarRecuadrosDeteccion(self, frame, listadoCoordenadasRostros):
        if len(listadoCoordenadasRostros) > 0:
            for (startX, startY, endX, endY, confianzaEsteRostro) in listadoCoordenadasRostros:
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

                text = "Face: " + "{:.2f}%".format(confianzaEsteRostro * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

                rostroColor = frame[startY:endY, startX:endX]
        return frame