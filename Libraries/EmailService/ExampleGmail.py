from Libraries.EmailService.LibraryGmail.Gmail import ServicioEmail, ProtocoloCorreo

mensaje = ProtocoloCorreo().MensajeEnviar("Titulo", "contenido", "Final")

GMAIL = ServicioEmail("d2lzcm92aS5yb2RyaWd1ZXpAZ21haWwuY29t",
                             "RkM1SkI2RU0=", "WISROVI")



GMAIL.setDestinatario( "ivAdventure", "comprasfcvwilliam@gmail.com")
GMAIL.SendCorreo("Prueba", mensaje)

FILE = "files/prueba.xlsx"
GMAIL.setDestinatario("ivAdventure", "wisrovi.rodriguez@gmail.com")
GMAIL.SendCorreo(asunto="Prueba", mensaje="hola mundo", archivoAdjunto=FILE)