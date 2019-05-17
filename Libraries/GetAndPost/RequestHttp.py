import requests


class RequestHttp:
    """

    AUTHOR: WISROVI

    """

    isHttps = False
    verify = None

    def __init__(self, isHttps, certificateRoute=None):
        self.isHttps = isHttps
        self.verify = certificateRoute

    def SendGet(self, url):
        respuestaGet = None
        if self.isHttps:
            respuestaGet = requests.get(url, verify = self.isHttps, cert=self.verify)
        else:
            respuestaGet = requests.get(url, verify=False)
        return respuestaGet.content

    def SendPost(self, url, json):
        respuestaGet = requests.post(url, data=json)
        return respuestaGet.content

