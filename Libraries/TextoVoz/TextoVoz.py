class TextoVoz:
    """
    Funciona sin conexión, a diferencia de otras bibliotecas de texto a voz. 
    En lugar de guardar el texto como archivo de audio, pyttsx lo dice allí. 
    Esto lo hace más confiable de usar para proyectos basados en voz.
    """
    try:
        import pyttsx3
    except:
        import os 
        os.system('pip3 install pyttsx3')
        os.system('pip3 install pypiwin32')
    
    idioma = ""
        
    def __init__(self, rate=120, volumen=0.9):
        self.engine = self.pyttsx3.init()
        self.engine.setProperty('rate', rate) #porcentaje velocidad a configurar
        self.engine.setProperty('volume', 0.9)  # Volumen 0-1
        
    def getRate(self):
        rate = self.engine.getProperty('rate')   #ver rate actual
        return rate
    
    def getVolumen(self):
        volume = self.engine.getProperty('volume')  #ver volumen actual
        return volume
    
    def getVocesDisponibles(self):
        voices = self.engine.getProperty('voices')
        contador = 0
        for voice in voices:
            print("Voice " + str(contador) + ":")
            print(" - ID: %s" % voice.id)
            print(" - Nombre: %s" % voice.name)
            print(" - Idioma: %s" % voice.languages)
            print(" - Gender: %s" % voice.gender)
            print(" - Age: %s" % voice.age)
            contador += 1
            
    def setIdioma(self, voz="es"):
        voz = str(voz).lower()
        
        voice_id = ""
        if voz.__eq__("es"):
            voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
        elif voz.__eq__("en"):
            voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        
        listVoces = []
        voices = self.engine.getProperty('voices')
        for voice in voices:
            listVoces.append(voice.id)
        
        if voice_id in listVoces:   
            self.engine.setProperty('voice', voice_id)         
            self.idioma = voz
        else:
            print("No existe la voz seleccionada, favor elija otra voz o instale la voz seleccionada.")
    
    def getIdioma(self):
        voice = self.engine.getProperty('voice')  #ver voz actual configurada
        return voice
        
    def Pronuncia(self, mensaje):
        if self.idioma.__eq__(""):
            import random
            voices = self.engine.getProperty('voices')
            choose_voice_id = random.randint(0, len(voices)-1)
            self.engine.setProperty('voice', voices[choose_voice_id].id)
        self.engine.say(mensaje)
        self.engine.runAndWait()
        
    def DetenerReproduccionVoz(self):
        self.engine.stop()