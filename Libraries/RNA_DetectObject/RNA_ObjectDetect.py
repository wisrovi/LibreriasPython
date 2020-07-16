import numpy as np
import cv2
import os.path as path

class ObjectDetect():
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    def __init__(self, confianza=0.2):
        BASE_DIR = path.dirname(path.realpath(__file__))
        protocolo = BASE_DIR + "/" + "MobileNetSSD_deploy.prototxt.txt" # arquitectura del modelo
        model = BASE_DIR + "/" + "MobileNetSSD_deploy.caffemodel" # pesos
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

    def ExtractObjectCoordinates(self, image, filterPerson=False):
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(
                cv2.resize(image, (300, 300)), # rescalamos el rostro al dimen int de la RNA
                0.007843, # normalizamos la imagen
                (300, 300),
                127.5 # le entregamos la resta media (R, G, B) con la que se entrenó la RNa para acoplar los colores del face esta media
            ) # blob = nuestra imagen de entrada después de la resta media, la normalización y el intercambio de canales.
        self.net.setInput(blob)
        self.detections = self.net.forward()

        listadoCoordenadas = list()
        for i in range(0, self.detections.shape[2]):
            confidence = self.detections[0, 0, i, 2]
            if confidence >= self.confianza:
                confidence = float("{:.2f}".format(confidence * 100))

                box = self.detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")       
                idx = int(self.detections[0, 0, i, 1])
                data = (startX, startY, endX, endY, confidence, idx)
                if not filterPerson:
                    listadoCoordenadas.append(data)
                else:
                    if idx == 15:
                        listadoCoordenadas.append(data)
        return listadoCoordenadas

    def PintarDetections(self, image, listadoCoordenadas):
        for (startX, startY, endX, endY, confidence, idx) in listadoCoordenadas:        
            label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence)
            cv2.rectangle(image, (startX, startY), (endX, endY),
                    self.COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)
        return image