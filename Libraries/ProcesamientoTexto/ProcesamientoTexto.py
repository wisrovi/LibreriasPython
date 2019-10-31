#pip install textblob
#python -m textblob.download_corpora

class ProcesamientoTexto:
    from textblob import TextBlob
    from textblob import Word
    from textblob.wordnet import VERB
    
    def __init__(self):
        self.text = None
    
    def setTex(self, texto):
        self.text = self.TextBlob(texto)
        
    def getEtiquetas(self):
        if self.text is not None:
            return self.text.tags
        else:
            return None
    
    def getFraseSustantiva(self):
        if self.text is not None:
            return self.text.noun_phrases
        else:
            return None
        
    def getIdiomaDetectado(self):
        if self.text is not None:
            return self.text.detect_language()
        else:
            return None
        
    def traducirTexto(self, nuevoIdioma="es", idiomaOrigen=None, texto=None):
        if self.text is not None:
            if nuevoIdioma is not None:                
                if texto is not None:
                    texto = self.TextBlob(texto)
                    if idiomaOrigen is not None:
                        return texto.translate(to=nuevoIdioma, from_lang=idiomaOrigen)
                    else:
                        return texto.translate(to=nuevoIdioma)
                else:
                    if idiomaOrigen is not None:
                        return self.text.translate(to=nuevoIdioma, from_lang=idiomaOrigen)
                    else:
                        return self.text.translate(to=nuevoIdioma)
            else:
                return None
        else:
            return None
        
    def dividirEnPaquetesDeTantasPalabras(self, numero=None):
        if self.text is not None:
            if numero is not None:
                return self.text.ngrams(n=numero)
            else:
                return None
        else:
            return None
        
    def getAnalisisSentimientos(self, objetivo=None, subjetivo=None, texto=None):
        """
        analiza el texto y devuelve que tan objetivo o subjetivo es
        0=muy objetivo
        1=muy subjetivo
        """
        if texto != None:
            texto = self.TextBlob(texto)
            if objetivo is not None:
                #pido el nivel de mensaje objetivo
                if subjetivo is not None:
                    #pido tambien el nivel de mensaje subobjetivo
                    return texto.sentiment
                else:
                    #pido unicamente el nivel de mensaje objetivo
                    return texto.sentiment.polarity
            elif subjetivo is not None:
                #pido unicamente el nivel de mensaje subobjetivo
                return texto.subjectivity
            else:
                #al no definir el filtro, entrego toda la respuesta
                return texto.sentiment
        elif self.text is not None:
            if objetivo is not None:
                #pido el nivel de mensaje objetivo
                if subjetivo is not None:
                    #pido tambien el nivel de mensaje subobjetivo
                    return self.text.sentiment
                else:
                    #pido unicamente el nivel de mensaje objetivo
                    return self.text.sentiment.polarity
            elif subjetivo is not None:
                #pido unicamente el nivel de mensaje subobjetivo
                return self.text.sentiment.subjectivity
            else:
                #al no definir el filtro, entrego toda la respuesta
                return self.text.sentiment
        else:
            return None
    def getPalabras(self):
        """
        get palabras tokenizacion
        """
        if self.text is not None:
            return self.text.words
        else:
            return None
        
    def getOraciones(self):
        """
        get oraciones tokenizacion
        """
        if self.text is not None:
            return self.text.sentences
        else:
            return None
        
    def convertirPalabraEnSingular(self, palabra=None):
        if palabra is not None:
            palabra = self.TextBlob(palabra)
            palabra = palabra.words[0]
            return palabra.singularize()
        else:
            return None
    
    def convertirPalabraEnPlural(self, palabra=None):
        if palabra is not None:
            palabra = self.TextBlob(palabra)
            palabra = palabra.words[0]
            return palabra.pluralize()
        else:
            return None
        
    def getLemmatize(self, palabra=None, isVerbo=None):
        if self.text is not None:
            if palabra is not None:
                palabra = self.Word(palabra)
                if isVerbo is not None:
                    return palabra.lemmatize("v")  #Pass in WordNet part of speech (verb)
                else:
                    return palabra.lemmatize()
            else:
                return None
        else:
            return None
        
    def  getDefinicionPalabra(self, palabra=None):
        if self.text is not None:
            if palabra is not None:
                palabra = self.Word(palabra)
                return palabra.definitions
            else:
                return None            
        else:
            return None
            
    def pluralizarOracion(self, oracion=None):
        if self.text is not None:
            if oracion is not None:
                oracion = self.TextBlob(oracion)
                oracion = oracion.words
                return oracion.pluralize()
            else:
                return None            
        else:
            return None
        
    def CorregirOrtografiaOracion(self, oracion=None):
        """
        La corrección ortográfica se basa en "Cómo escribir un corrector ortográfico" de Peter Norvig [1] tal como está implementado en la biblioteca de patrones. Tiene aproximadamente un 70% de precisión
        """
        if self.text is not None:
            if oracion is not None:
                oracion = self.TextBlob(oracion)
                return oracion.correct()
            else:
                return None            
        else:
            return None
        
    def CorregirOrtografiaPalabra(self, palabra=None):
        """
        La corrección ortográfica se basa en "Cómo escribir un corrector ortográfico" de Peter Norvig [1] tal como está implementado en la biblioteca de patrones. Tiene aproximadamente un 70% de precisión
        """
        if self.text is not None:
            if palabra is not None:
                palabra = self.Word(palabra)
                return palabra.spellcheck()
            else:
                return None            
        else:
            return None
        
    def ContarPalabrasOracion(self, oracion=None, palabrasBuscarContar=None, sensibleMayusculas=False):
        if self.text is not None:
            if oracion is not None:
                if palabrasBuscarContar is not None:
                    oracion = self.TextBlob(oracion)
                    if len(self.TextBlob(palabrasBuscarContar).words) > 1:
                        return oracion.noun_phrases.count(palabrasBuscarContar)
                    else:
                        if sensibleMayusculas:
                            #return oracion.word_counts[palabraBuscarContar]
                            return oracion.words.count(palabrasBuscarContar, case_sensitive=True)  
                        else:
                            return oracion.words.count(palabrasBuscarContar)
                else:
                    return None
            else:
                return None            
        else:
            return None
        
    
if __name__ == '__main__':
    pt = ProcesamientoTexto()
    pt.setTex("Hola mundo, esto es una prueba de funcionamiento de la libreria. Estamos evaluando el sistema.")
    print("Etiquetas:", pt.getEtiquetas())
    print("Frase sustantiva:", pt.getFraseSustantiva())
    print("Idioma Detectado:", pt.getIdiomaDetectado())
    
    print("Analisis Sentimientos objetivo:", pt.getAnalisisSentimientos(objetivo=True))
    print("Analisis Sentimientos subjetivo:", pt.getAnalisisSentimientos(subjetivo=True))
    print("Analisis Sentimientos:", pt.getAnalisisSentimientos(objetivo=True, subjetivo=True))
    print("Analisis Sentimientos:", pt.getAnalisisSentimientos())
    print("Analisis Sentimientos:", pt.getAnalisisSentimientos(texto="Hoy es un día maravilloso."))
    
    print("Extraer palabras:", pt.getPalabras())
    print("Extraer Oraciones:", pt.getOraciones())
    
    print("Palabra singular:", pt.convertirPalabraEnSingular("People"))
    print("Palabra Plural:", pt.convertirPalabraEnPlural("Play"))
    
    print("Palabra Lemmatize:", pt.getLemmatize(palabra = "Play"))
    print("Palabra Lemmatize:", pt.getLemmatize(palabra = "Play", isVerbo=True))
    
    print("Definicion Palabra:", pt.getDefinicionPalabra(palabra = "octopus"))
    
    print("Pluralizar Oracion:", pt.pluralizarOracion(oracion = "octopus have 8 hands"))
    
    print("Corrector ortografico Oracion:", pt.CorregirOrtografiaOracion(oracion="I havv goood speling!"))
    
    print("Corrector ortografico Palabra:", pt.CorregirOrtografiaPalabra(palabra="falibility"))
    
    print("Contador Palabras:", pt.ContarPalabrasOracion(oracion="We are no longer the Knights who say Ni. We are now the Knights who say Ekki ekki ekki PTANG.", palabrasBuscarContar="ekki"))
    
    
          
          
          
          
          