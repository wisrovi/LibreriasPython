from classReconocimientoFacial import ReconocimientoFacial
fr = ReconocimientoFacial(BaseDatos='ReconocimientoFacial.db', tablaBaseDatos="Personas")


from flask import Flask, jsonify, request, redirect
# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)

nombreParametrosRecibirPost = {
    "Imagen" : 'file',
    "NombreImagen" : "nameFile"
}

htmlRta = {
    "index" :
    '''
    <!doctype html>
    <title>Servidor IA</title>
    <h1>Servidor de Reconocimiento Facial WISROVI</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=%s>
         <input type=submit value=Upload>
    </form>
    ''' %(nombreParametrosRecibirPost["Imagen"]),
    
    "registrar" :
    '''
    <!doctype html>
    <title>Servidor IA</title>
    <h1>Servidor de Reconocimiento Facial WISROVI</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=%s>
         <input type=text name=%s>
         <input type=submit value=Upload>
    </form>
    ''' %(nombreParametrosRecibirPost["Imagen"], nombreParametrosRecibirPost["NombreImagen"]),
    
    "registrar_2" :
    '''
    <!doctype html>
    <title>Servidor IA</title>
    <h1>Servidor de Reconocimiento Facial WISROVI</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=%s>
         <input type=submit value=Upload>
    </form>
    ''' %(nombreParametrosRecibirPost["Imagen"])
    
    
}




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/error', methods=['GET', 'POST'])
def error():
    return fr.getDicError()

@app.route('/index', methods=['GET', 'POST'])
def index():    
    if request.method == 'POST':
        if nombreParametrosRecibirPost["Imagen"] not in request.files:
            return redirect(request.url)
        else:
            rutaImagen = request.files[nombreParametrosRecibirPost["Imagen"]]
            if rutaImagen.filename == '':
                return redirect(request.url)
            if rutaImagen and allowed_file(rutaImagen.filename):                
                rtaJson = fr.ReconocerPersona(rutaImagen)                
                ipCliente = request.environ['REMOTE_ADDR']
                return rtaJson
    
    return htmlRta["index"]

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        if nombreParametrosRecibirPost["Imagen"] not in request.files:
            return redirect(request.url)
        else:
            rutaImagen = request.files[nombreParametrosRecibirPost["Imagen"]]
            if rutaImagen.filename == '':
                return redirect(request.url)
            if rutaImagen and allowed_file(rutaImagen.filename):
                #nombreFoto = request.form['nameFile']
                rtaJson = fr.RegistrarNuevaPersona(rutaImagen)
            ipCliente = request.environ['REMOTE_ADDR']
            return rtaJson
    
    return htmlRta["registrar_2"]



if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=1990, debug=True)
