
import telebot



class TelegramService():
    """

    AUTHOR: WISROVI

    """
    Token = ""
    tb = None
    def __init__(self, token):
        self.Token = token
        self.tb = telebot.TeleBot(self.Token)

    def sendMessage(self, Id_group, Mensaje):
        if self.tb != None:
            self.tb.send_message(Id_group, Mensaje)

    def sendAudio(self,Id_group, rutaAudio ):
        self.tb.send_audio(chat_id=Id_group, audio=open(rutaAudio, 'rb'))

    def e(self, IdDestino, message):
        self.tb.reply_to(IdDestino, message)