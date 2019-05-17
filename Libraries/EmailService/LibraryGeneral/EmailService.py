import smtplib
import base64

class ServicioEmail():
    emailOrigen = "d2lzcm92aS5yb2RyaWd1ZXpAZ21haWwuY29t"
    pwdCorreo = "RkM1SkI2RU0="
    nombreRemitente = 'V0lTUk9WSQ=='

    def __init__(self, emailOrigenBase64, passwordEmailBase64, nombreRemitenteBase64):
        self.emailOrigen = emailOrigenBase64
        self.pwdCorreo = passwordEmailBase64
        self.nombreRemitente = nombreRemitenteBase64

    def decoBase64UrlSafe(self, s):
        var = base64.urlsafe_b64decode(s + '=' * (4 - len(s) % 4))
        return str(var, 'utf-8')

    def sendEmail(self, nombreGrupo, emailto, subject, body):
        email_user = self.decoBase64UrlSafe(self.emailOrigen)
        email_password = self.decoBase64UrlSafe(self.pwdCorreo)
        namefrom = self.decoBase64UrlSafe(self.nombreRemitente)

        # emailto = ['wisrovi.rodriguez@gmail.com', 'comprasfcvwilliam@gmail.com']

        message = """From: %s <%s>
To: %s <%s>
MIME-Version: 1.0
Content-type: text/html
Subject: %s

%s
        """ % (namefrom, email_user, nombreGrupo, emailto.split(), subject, body)
        try:
            #print("*********** Nuevo Correo *****************")
            serverGmail = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
            #print("Enviando desde: ", email_user)
            serverGmail.ehlo()
            #print("con asunto: ", subject)
            serverGmail.login(email_user, email_password)
            #print("destinatario: ", emailto.split())
            serverGmail.sendmail(email_user, emailto.split(), message)
            #print("con titulo: ", nombreGrupo)
            serverGmail.close()

            #print("******************************************")
            return "OK"
            # serverGmail.starttls()
        except:
            return "BAD"






