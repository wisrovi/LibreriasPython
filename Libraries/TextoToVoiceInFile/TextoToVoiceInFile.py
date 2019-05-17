from gtts import gTTS


class TextoToVoiceInFile:
    """

    AUTHOR: WISROVI

    """
    def convertTextToVoiceAndSaveFile(self, nombreArchivo, texto):
        tts = gTTS(text=texto, lang='es')
        self.rutaArchivo = nombreArchivo + ".mp3"
        tts.save(self.rutaArchivo)
        return self.rutaArchivo

