"""
/*
 * Copyright (c) Forge Development LLC
 * SPDX-License-Identifier: LGPL-2.1-only
 */
package net.minecraftforge.installer.json;

import java.net.URL;

import javax.imageio.ImageIO;
import javax.swing.Icon;
import javax.swing.ImageIcon;

public class Mirror {
    private String name;
    private String image;
    private String homepage;
    private String url;
    private boolean triedImage;
    private Icon _image_;

    public Mirror() {}

    public Mirror(String name, String image, String homepage, String url) {
        this.name = name;
        this.image = image;
        this.homepage = homepage;
        this.url = url;
    }

    public Icon getImage() {
        if (!triedImage) {
            try {
                if (getImageAddress() != null)
                    _image_ = new ImageIcon(ImageIO.read(new URL(getImageAddress())));
            } catch (Exception e) {
                _image_ = null;
            } finally {
                triedImage = true;
            }
        }
        return _image_;
    }

    public String getName() {
        return name;
    }
    public String getImageAddress() {
        return image;
    }
    public String getHomepage() {
        return homepage;
    }
    public String getUrl() {
        return url;
    }
}

"""
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
                    image_bytes = bytes()
                    self._image_ = QImage.fromData(base64.b64encode(self.image.replace("data:image/png;base64","")))
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
