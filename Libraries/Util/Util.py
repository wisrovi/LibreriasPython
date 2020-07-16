from datetime import datetime
from imutils import paths
import cv2

def wait_for_change_image(endSeconds, dateStart):
    dateNow = datetime.now()
    diff = dateNow - dateStart
    seconds = diff.seconds
    if seconds > endSeconds:
        return True
    return False

def ListarImagenesDirectorio(dir):
    return sorted(list(paths.list_images(dir + "/")))

def AnotarNivelBorroso(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    cv2.putText(image, "Blurry: {:.2f}".format(fm), (10, 30),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    return image

def EmparejarDosListas(lista1, lista2):
    return zip(lista1, lista2)