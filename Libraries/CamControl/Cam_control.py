class Cam_control():
    import os
    import cv2
    from imutils.video import FPS

    fps = None
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
    resolucionCamara = {
        "MIN" : (320,240),      #Mini
        "BAS" : (640,480),      #Basic
        "hd" : (1366,768),      #HD
        "720p" : (1280,720),    #HD+
        "1080p" : (1920,1080),  #full HD
        "1440p" : (2560,1440),  #QHD o 2K
        "UHD" : (3840,2160),
        "8K" : (7680,4320)
    }

    def __init__(self):
        self.fps = self.FPS().start()

    def ReadImage(self, imagePath=None):
        image = None
        if imagePath is not None:
            image = self.cv2.imread(imagePath)
        return image

    def ConfigCam(self, rutaCamara=None, usarWebCam=True, calidadWebCam="BAS", userRNA=False): # calidadWebCam = [MIN, BAS, hd, 720p, 1080p, 1440p, UHD, 8K]
        if usarWebCam:
            self.vcap = self.cv2.VideoCapture(0)
            self.vcap.set(int(3), self.resolucionCamara[calidadWebCam][0]) 
            self.vcap.set(int(4), self.resolucionCamara[calidadWebCam][1])
            if userRNA:
                self.vcap.set(int(5), 10)
            else:
                self.vcap.set(int(5), 32)
            self.cam_correct = True
        else:
            if rutaCamara is not None:
                self.vcap = self.cv2.VideoCapture(rutaCamara) # puede ser RTSP_route o video_route
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
                fourcc = self.cv2.VideoWriter_fourcc(*"MJPG")
                if frame is not None:
                    self.writer = self.cv2.VideoWriter(namePathVideo, fourcc, 25,(frame.shape[1], frame.shape[0]), True)
                else:
                    if self.image is not None:
                        self.writer = self.cv2.VideoWriter(namePathVideo, fourcc, 25,(self.image.shape[1], self.image.shape[0]), True)
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
                    self.fps.update()
                else:
                    self.image = None
            return self.image

    def DetenerCamara(self):
        if self.cam_correct:
            self.fps.stop()
            resumeFPS = (  self.fps.elapsed(), self.fps.fps()  )
            self.vcap.release()
            self.cv2.destroyAllWindows()  # Destruyo la ventana
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
                net.setPreferableTarget(self.cv2.dnn.DNN_TARGET_MYRIAD)

    def search_key_finish_process(self):
        if self.cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        return False

    def MostrarFrame(self, ponerFirma=True, nameWindow="ventana"):
        if self.image is not None:
            if ponerFirma:
                self.PonerTextoImagen(texto="www.wisrovi.com",posicion=(self.image.shape[1] - 135, self.image.shape[0] - 10))
            self.cv2.imshow(nameWindow, self.image)
    def ResizeImage(self, widthDream=720):
        scale_percent = int(widthDream * 100 / self.image.shape[1])
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dsize = (width, height)
        self.image = self.cv2.resize(self.image, dsize)

    def GetBlurry(self): # nivel borrosa de la imagen
        gray = self.cv2.cvtColor(self.image, self.cv2.COLOR_BGR2GRAY)
        fm = self.cv2.Laplacian(gray, self.cv2.CV_64F).var()
        return float("{:.2f}".format(fm))

    def PonerTextoImagen(self, texto="prueba",
                            posicion=(20, 20),
                            tipoLetra =tiposLetra["hershey"][0],
                            escalaLetra=tiposLetra["hershey"][1],
                            colorLetra=tiposLetra["hershey"][2],
                            gruesoLetra = tiposLetra["hershey"][3]):
        self.cv2.putText(self.image,
                    texto,
                    posicion,
                    tipoLetra,
                    escalaLetra,
                    colorLetra,
                    gruesoLetra)


