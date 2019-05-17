
import smtplib, getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

user = "wisrovi.rodriguez@gmail.com"
password = "FC5JB6EM"

remitente = "WISROVI <" + "wisrovi.rodriguez@gmail.com" + ">"
destinatario = "ivAdventure <" + "wisrovi.rodriguez@gmail.com" + ">"
asunto = "prueba"
mensaje = "<h1> Prueba </h1>" \
          "<p1> hola </p1>"

gmail = smtplib.SMTP_SSL('smtp.gmail.com', 465)
gmail.login(user, password)

gmail.set_debuglevel(1)
header = MIMEMultipart()
header['Subject'] = asunto
header['From'] = remitente
header['To'] = destinatario

mensaje = MIMEText(mensaje, 'html')
header.attach(mensaje)

gmail.sendmail(remitente, destinatario, header.as_string())

gmail.quit()