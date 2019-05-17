from Libraries.EmailService.LibraryGeneral.EmailService import ServicioEmail

email = ServicioEmail(emailOrigenBase64 = "d2lzcm92aS5yb2RyaWd1ZXpAZ21haWwuY29t",
                      passwordEmailBase64 = "RkM1SkI2RU0=",
                      nombreRemitenteBase64 = 'V0lTUk9WSQ==')

tituloMensaje = 'Final Trabajo'
destinatario = "wisrovi.rodriguez@gmail.com"
asunto = 'Final trabajo WISROVI'
body = 'son las 10:30pm'

rta = email.sendEmail(tituloMensaje, destinatario, asunto, body )
print(rta)


