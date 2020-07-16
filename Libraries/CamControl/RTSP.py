class Camara:
    def __init__(self, proveedor, user, password, ip, nombre_camara=None, channel=1):
        self.proveedor = proveedor
        self.user = user
        self.password = password
        self.ip = ip
        self.nombre_camara = nombre_camara
        self.channel = channel

    def get_url_rtsp(self):
        return str(self.proveedor).format(self.user, self.password, self.ip, self.channel)


proveedores = dict()
proveedores["HiVision"] = "rtsp://{}:{}@{}:554/Streaming/Channels/{}"
proveedores["Dahua"] = "rtsp://{}:{}@{}:554/cam/realmonitor?channel={}&subtype=0"

CAMARAS = list()
CAMARAS.append(Camara(
    proveedor=proveedores["HiVision"],
    user="admin",
    password="admin",
    ip="192.168.1.26",
    nombre_camara="Cam 2"))
CAMARAS.append(Camara(
    proveedor=proveedores["Dahua"],
    user="admin",
    password="admin",
    ip="192.168.1.25",
    nombre_camara="Cam 1"))

if __name__ == '__main__':
    for cam in CAMARAS:
        print(cam.nombre_camara, cam.get_url_rtsp())
