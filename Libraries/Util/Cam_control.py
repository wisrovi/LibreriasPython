from Util.Count_FPS import Count_FPS
import cv2



class Cam_control():
    import os
    fps = Count_FPS()
    writer = None
    pathSaveVideo = None
    cam_correct = False
    pathSave = "videoOut"
    colores = {  # Blue Green Red
        "rojo": (3, 37, 254),
        "amarillo": (0, 201, 255),
        "verde": (3, 254, 3),
        "blanco": (255, 255, 255),
        "fuccia": (255, 0, 255)
    }
    tiposLetra = {  # tipo_letra, tamaño, color, grosor
        "hershey": (cv2.FONT_HERSHEY_SIMPLEX, 0.5, colores["rojo"], 2)
    }

    def __init__(self, rutaCamara=None, usarWebCam=True):
        if usarWebCam:
            self.vcap = cv2.VideoCapture(0)
            self.cam_correct = True
        else:
            if rutaCamara is not None:
                self.vcap = cv2.VideoCapture(rutaCamara) # puede ser RTSP_route o video_route
                self.cam_correct = True

    def __CreatePathIfNotExist(self, path=None):
        if self.cam_correct:
            if path is not None:
                self.pathSave = path
            try:
                self.os.stat(self.pathSave)
            except:
                self.os.mkdir(self.pathSave)
            self.pathSaveVideo = self.pathSave

    def SaveFotogramaVideo(self, namePathVideo=None, nameFileVideo='output.avi', frame=None):
        if self.cam_correct:
            self.__CreatePathIfNotExist(namePathVideo)
            if self.writer is None:
                namePathVideo = self.pathSaveVideo + "/" + nameFileVideo
                fourcc = cv2.VideoWriter_fourcc(*"MJPG")
                if frame is not None:
                    self.writer = cv2.VideoWriter(namePathVideo, fourcc, 25,(frame.shape[1], frame.shape[0]), True)
                else:
                    if self.image is not None:
                        self.writer = cv2.VideoWriter(namePathVideo, fourcc, 25,(self.image.shape[1], self.image.shape[0]), True)
            else:
                if frame is not None:
                    self.writer.write(frame)
                else:
                    if self.image is not None:
                        self.writer.write(self.image)

    def CaptureFotograma(self, procesarCaptura=True):
        if self.cam_correct:
            ret, self.image = self.vcap.read()
            if self.image is not None:
                if procesarCaptura:
                    self.fps.Update()
                else:
                    self.image = None
            return self.image

    def DetenerCamara(self):
        if self.cam_correct:
            self.fps.Stop()
            resumeFPS = self.fps.Resume()
            self.vcap.release()
            cv2.destroyAllWindows()  # Destruyo la ventana
            if self.writer is not None:
                self.__CreatePathIfNotExist()
                file = open(self.pathSaveVideo + "/" + "infoVideoOut.txt", "w")
                file.write("Tiempo video: {}".format(resumeFPS[0]) + self.os.linesep)
                file.write("FPS video: {}".format(resumeFPS[1]) + self.os.linesep)
                file.close()
            return resumeFPS
        else:
            return (None, None)

    def Usar_MOVIDIUS(self, net=None):
        if self.cam_correct:
            if net is not None:
                net.setPreferableTarget(cv2.dnn.DNN_TARGET_MYRIAD)

    def search_key_finish_process(self):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        return False

    def MostrarFrame(self, ponerFirma=True, nameWindow="ventana"):
        if self.image is not None:
            if ponerFirma:
                self.PonerTextoImagen(texto="www.wisrovi.com",posicion=(self.image.shape[1] - 135, self.image.shape[0] - 10))
            cv2.imshow(nameWindow, self.image)
    def ResizeImage(self, widthDream=720):
        scale_percent = int(widthDream * 100 / self.image.shape[1])
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dsize = (width, height)
        self.image = cv2.resize(self.image, dsize)

    def GetBlurry(self): # nivel borrosa de la imagen
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        fm = cv2.Laplacian(gray, cv2.CV_64F).var()
        return float("{:.2f}".format(fm))

    def PonerTextoImagen(self, texto="prueba",
                            posicion=(20, 20),
                            tipoLetra =tiposLetra["hershey"][0],
                            escalaLetra=tiposLetra["hershey"][1],
                            colorLetra=tiposLetra["hershey"][2],
                            gruesoLetra = tiposLetra["hershey"][3]):
        cv2.putText(self.image,
                    texto,
                    posicion,
                    tipoLetra,
                    escalaLetra,
                    colorLetra,
                    gruesoLetra)


