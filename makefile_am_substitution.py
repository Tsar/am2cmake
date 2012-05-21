#!/usr/bin/env python2.7

import os, string, re

def scanDir(path):
    mkfList = []
    fileNames = [path + "/Makefile.am", path + "/makefile.am"]
    for fileName in fileNames:
        if os.path.exists(fileName):
            mkfList.append(fileName)
    l = os.listdir(path)
    for pth in l:
        fpth = path + "/" + pth
        if os.path.isdir(fpth):
            mkfList.extend(scanDir(fpth))
    return mkfList

def needReplacement(mkf):
    res = set()
    with open(mkf, "r") as f:
        s = f.read()
    l = re.findall(r'\$\(\S+?\)', s)
    for x in l:
        res.add(x)
    return res

if __name__ == "__main__":
    mkfList = scanDir("/home/volkov/work/dev/ext/src/GraphicsMagick-1.3.14")
    nr = set()
    for mkf in mkfList:
        nr |= needReplacement(mkf)
    print nr
