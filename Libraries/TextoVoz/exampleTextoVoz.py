from TextoVoz import TextoVoz

if __name__ == '__main__':
    tv = TextoVoz(rate=120, volumen=0.6)
    tv.setIdioma("es")  #si no se parametriza esto, el sistema eligira una voz al azar dentro de las voces disponibles
    #print(tv.getRate())
    #print(tv.getVolumen())
    #print(tv.getIdioma())
    #tv.getVocesDisponibles()
    tv.Pronuncia('Cordial saludo WISROVI, bienvenido al sistema inteligente SAM')