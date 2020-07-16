from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import os.path as path

BASE_DIR = path.dirname(path.realpath(__file__))
MODEL_DETECT_MASK = BASE_DIR + "/" + "mask_detector.model"
maskNet = load_model(MODEL_DETECT_MASK) if path.exists(MODEL_DETECT_MASK) else None
if maskNet is None:
    print("No se encontró la libreria de Mask")

import cv2


def PreprocesarRostro(face):
    face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
    face = cv2.resize(face, (224, 224))
    face = img_to_array(face)
    face = preprocess_input(face)
    return face


def ClasificarRostros(faces):
    preds = None
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    return preds

def BuscarMascarillaRostros(listadoCoordenadasRostros, frame):
    if len(listadoCoordenadasRostros) > 0:
        faces = []  # Para buscar mascarilla facial
        locs = []  # Para buscar mascarilla facial
        for (startX, startY, endX, endY, confianzaEsteRostro) in listadoCoordenadasRostros:
            face = frame[startY:endY, startX:endX]

            face = MaskDetector.PreprocesarRostro(face)
            faces.append(face)
            locs.append((startX, startY, endX, endY))

        preds = MaskDetector.ClasificarRostros(faces)

        for (box, pred) in zip(locs, preds):
            (startX, startY, endX, endY) = box
            (mask, withoutMask) = pred
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
            cv2.putText(frame, label, (startX, startY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
    return frame
