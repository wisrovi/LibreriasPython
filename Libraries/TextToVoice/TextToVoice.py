
import win32com.client as wincl


speak = wincl.Dispatch("SAPI.SpVoice")

class TextToVoice:
    """

    AUTHOR: WISROVI

    """
    def talking(self, text):
        audio = speak.Speak(text)



