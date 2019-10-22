class Rta:
    import json
    personaExiste = False
    etiqueta = "-"
    error = 0
    
    def getJson(self):
        obj = {
            "personaExiste" : self.personaExiste,
            "etiqueta" : self.etiqueta,
            "error" : self.error
        }
        return self.json.dumps(obj)

class ReconocimientoFacial:
    """
    Esta Class utiliza la libreria de face_recognition
    con la diferencia de almacenar los parametros en una base de datos definida por el usuario
    
    Todo esto fue creado y parametrizado por William Rodriguez (WISROVI)
    """
    
    from classSQLITE import SQLITE
    import pandas as pd
    import numpy as np
    import face_recognition
    import json
    
    diccionarioErrores = {
        0 : None,
        1 : "No se recibio imagen",
        2 : "Persona no existe en la Base de Datos",
        3 : "No se puede registrar porque ya esta registrada",
        4 : "La imagen entregada no es valida",
        5 : "La imagen no tiene un rostro",
        6 : "Se encontro un rostro, pero la resolución de la imagen no permite extraer los puntos caracteristicos",
        7 : "La persona no se puede crear, ya existe en la base de datos"
    }
    
    vectorCaracteristicas = []
    vectorNombres = []
    def __init__(self, BaseDatos='pruebaDB.db', tablaBaseDatos="tabla1"):
        self.baseDatos = BaseDatos
        self.tabla = tablaBaseDatos
        self.DB = self.SQLITE(self.baseDatos, self.tabla)
        self.DB.CrearTabla()  #se crea solo si no existe
    
    def __LeerBaseDatosActual(self):
        df = self.DB.LeerDB()
        for i, row in df.iterrows():
            for nombreColumna, valorColumna in row.iteritems():
                if nombreColumna.__eq__("id"):
                    self.vectorNombres.append(valorColumna)
                    
                if nombreColumna.__eq__("vector"):
                    vectorString = list(valorColumna.split(","))
                    vectorFloat = [float(i) for i in vectorString]
                    vectorNumpy = self.np.asarray(vectorFloat)
                    self.vectorCaracteristicas.append(vectorNumpy)
                    
    def ReconocerPersona(self, rutaImagen = None):
        r = Rta()
        if rutaImagen is None:
            r.error = 1
            error = 1
            #print("Se requiere una imagen para aplicar el reconocimiento")
        else:
            self.__LeerBaseDatosActual()
            imagenCorrecta = False
            try:
                image = self.face_recognition.load_image_file(rutaImagen)
                imagenCorrecta = True
            except:
                r.error = 4                
            if imagenCorrecta:            
                face_locations = self.face_recognition.face_locations(image)
                if len(face_locations) > 0:
                    try:
                        person_encoding = self.face_recognition.face_encodings(image, face_locations)[0]
                        respuesta = self.face_recognition.compare_faces(self.vectorCaracteristicas, person_encoding, 0.50)
                    except:
                        r.error = 6                        
                    if r.error == 0:
                        if True in respuesta:
                            indice = respuesta.index(True)
                            nombre = self.vectorNombres[indice]
                            r.personaExiste = True
                            r.etiqueta = nombre
                        else:
                            r.error = 2
                            #print("Persona no existe en la base de datos.")
                else:
                    r.error = 5
        return r.getJson()
    
    def RegistrarNuevaPersona(self, rutaImagen = None):
        r = Rta()
        if rutaImagen is None:
            r.error = 1
            #print("Se requiere una imagen para poder registrarla")
        else:
            rtaJson = self.ReconocerPersona(rutaImagen)
            objeto = self.json.loads( rtaJson )
            print(rtaJson)
            if objeto["error"] == 2:            
                imagenCorrecta = False
                try:
                    image = self.face_recognition.load_image_file(rutaImagen)
                    imagenCorrecta = True
                except:
                    r.error = 4
                if imagenCorrecta:
                    face_locations = self.face_recognition.face_locations(image)
                    if len(face_locations) > 0:
                        try:
                            person_encoding = self.face_recognition.face_encodings(image, face_locations)[0]
                            respuesta = self.face_recognition.compare_faces(self.vectorCaracteristicas, person_encoding, 0.50)
                        except:
                            r.error = 6
                        if r.error == 0:
                            if True in respuesta:
                                indice = respuesta.index(True)
                                nombre = self.vectorNombres[indice]
                                r.error = 3
                                #print("La persona no se puede registrar porque ya esta registrada con id: " + str(nombre))
                            else:
                                person_encoding_list = list(person_encoding)
                                person_encoding_string = str(person_encoding_list).strip('[]')
                                id = self.DB.InsertarDatos(person_encoding_string)
                                r.personaExiste = True
                                r.etiqueta = str(id)
                                #print("Persona registrada correctamente con id: " + etiqueta)
                    else:
                        r.error = 5
            else:
                r.error = objeto["error"]
                if objeto["error"] != 5: 
                    r.error = 7                    
                r.personaExiste = objeto["personaExiste"]
                r.etiqueta = objeto["etiqueta"]
        return r.getJson()
                
    def getDicError(self):
        return self.json.dumps(self.diccionarioErrores)
    
    