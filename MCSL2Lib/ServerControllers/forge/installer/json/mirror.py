import base64

from PyQt5.QtGui import QImage


class Mirror:
    name = ""
    image = ""
    homepage = ""
    url = ""
    triedImage = False
    _image_ = None

    def __init__(self, name="", image="", homepage="", url=""):
        self.name = name
        self.image = image
        self.homepage = homepage
        self.url = url

    # TODO
    def getImage(self):
        if not self.triedImage:
            try:
                if self.getImageAddress():
                    # TODO
                    self._image_ = QImage.fromData(base64.b64encode(self.image.replace("data:image/png;base64", "")))
            except Exception as e:
                print(e.args)
                self._image_ = None
            finally:
                self.triedImage = True

        return self._image_

    def getName(self):
        return self.name

    def getImageAddress(self):
        return self.image

    def getHomepage(self):
        return self.homepage

    def getUrl(self):
        return self.url
