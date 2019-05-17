import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import os
from email.mime.base import MIMEBase
from email.encoders import encode_base64

import base64


class ProtocoloCorreo:
    def MensajeEnviar(self, tituloMensaje, contenidoMensaje, finalMensaje):
        mensaje = "<h1> " + tituloMensaje + " </h1>" \
                  "<p1> " + contenidoMensaje + " </p1>" \
                  "<h4> " + finalMensaje + " </h4>"
        return mensaje

    def Remitente(self, apodoRemitente, correoRemitente):
        return apodoRemitente + " <" + correoRemitente + ">"

    def Destinatario(self, etiquetaDestinatario, correoDestinatario):
        return etiquetaDestinatario + " <" + correoDestinatario + ">"

    def decoBase64UrlSafe(self, s):
        var = base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4))
        return str(var, 'utf-8')

    def ExisteVariable(self, variable):
        try:
            a = variable
            return True
        except:
            return False

class ServicioEmail(ProtocoloCorreo):
    """
    En el constructor de esta clase recibe las credenciales de conexion, email y password para acceder a la cuenta,
    asi como un apodo del dueño del email (para establecer el remitente)
    para esto: ServicioEmail(emailInBase64","passwordInBase64", "pseudonimo")

    Antes de preparar el correo se recomienda preparar el mensaje a enviar
    (no es obligatorio, pero para dar mas presentacion al mensaje es recomendado)
    para eso se usa: ProtocoloCorreo().MensajeEnviar

    Seguidamente se prepara el destinatario con: setDestinatario

    Finalmente se envia el correo con: SendCorreo(asunto="Prueba", mensaje="hola mundo", archivoAdjunto="ruta archivo")



    *********************************************
    example1:
    mensaje = ProtocoloCorreo().MensajeEnviar("Titulo", "contenido", "Final")
    GMAIL = ServicioEmail("emailInBase64",
                             "passwordInBase64", "pseudonimo")
    GMAIL.setDestinatario("apodoDestino", "EmailTo")
    GMAIL.SendCorreo(asunto="Prueba", mensaje="hola mundo")

    *********************************************
    example2:
    mensaje = ProtocoloCorreo().MensajeEnviar("Titulo", "contenido", "Final")
    GMAIL = ServicioEmail("emailInBase64",
                             "passwordInBase64", "pseudonimo")
    GMAIL.setDestinatario("apodoDestino", "EmailTo")
    GMAIL.SendCorreo(asunto="Prueba", mensaje="hola mundo")

    GMAIL.setDestinatario("apodoDestino2", "EmailTo2")
    GMAIL.SendCorreo(asunto="Prueba", mensaje="hola mundo")

    *********************************************
    example3:
    mensaje = ProtocoloCorreo().MensajeEnviar("Titulo", "contenido", "Final")
    GMAIL = ServicioEmail("emailInBase64",
                             "passwordInBase64", "pseudonimo")
    GMAIL.setDestinatario("ivAdventure", "wisrovi.rodriguez@gmail.com")

    FILE = "files/prueba.xlsx"
    GMAIL.SendCorreo(asunto="Prueba", mensaje="hola mundo", archivoAdjunto=FILE)
    *********************************************
    """

    def __init__(self, emailOrigenBase64, passwordEmailBase64, apodoRemitente, DEBUG = 0):
        self.user = self.decoBase64UrlSafe(emailOrigenBase64)
        self.password = self.decoBase64UrlSafe(passwordEmailBase64)
        self.remitente = self.Remitente(apodoRemitente, self.user)
        self.debug = DEBUG

    def setDestinatario(self, apodoDestinatario, destinatario):
        self.gmail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.gmail.login(self.user, self.password)
        if self.debug != 0:
            self.gmail.set_debuglevel(1)
        self.destinatario = self.Destinatario(apodoDestinatario, destinatario)

    def ConstruirHeader(self):
        try:
            a = self.header
        except:
            self.header = MIMEMultipart()

    def __AdjuntarArchivo(self, nombreArchivo):
        if os.path.isfile(nombreArchivo):
            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(open(nombreArchivo, 'rb').read())
            encode_base64(adjunto)
            adjunto.add_header('Content-Disposition',
                               'attachment; filename="%s"' %os.path.basename(nombreArchivo)
                               )
            self.ConstruirHeader()
            self.header.attach(adjunto)
            print("Archivo " + nombreArchivo)
        else:
            print("El archivo no existe")

    def SendCorreo(self,
                  asunto = "<vacio>",
                  mensaje = "<p1> <vacio> </p1>",
                  archivoAdjunto = None):

        try:
            mensaje = MIMEText(mensaje, 'html')

            self.ConstruirHeader()

            self.header['Subject'] = asunto
            self.header['From'] = self.remitente
            self.header['To'] = self.destinatario
            self.header.attach(mensaje)

            if archivoAdjunto != None:
                self.__AdjuntarArchivo(archivoAdjunto)

            self.gmail.sendmail(self.remitente, self.destinatario, self.header.as_string())
            self.gmail.quit()
            return True
        except:
            return False



