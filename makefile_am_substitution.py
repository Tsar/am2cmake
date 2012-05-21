#!/usr/bin/env python2.7

import os, string

def tryDir(path, old, new):
    fileNames = [path + "/Makefile.am", path + "/makefile.am"]
    for fileName in fileNames:
        if os.path.exists(fileName):
            with open(fileName, "r") as f:
                s = f.read()
                s = string.replace(s, old, new)
            with open(fileName, "w") as f:
                f.write(s)
    l = os.listdir(path)
    for pth in l:
        fpth = path + "/" + pth
        if os.path.isdir(fpth):
            tryDir(fpth, old, new)

if __name__ == "__main__":
    tryDir("/home/volkov/work/dev/ext/src/GraphicsMagick-1.3.14", "$(LIBMAGICK)", "magick/libGraphicsMagick.la")
    tryDir("/home/volkov/work/dev/ext/src/GraphicsMagick-1.3.14", "$(LIBMAGICKPP)", "Magick++/lib/libGraphicsMagick++.la")
