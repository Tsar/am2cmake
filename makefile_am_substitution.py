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

def getRidOfMultilines(mkf):
    with open(mkf, "r") as f:
        s = f.read()
    s = re.sub(r'\s*\\\s*\n\s*', r' ', s)
    with open(mkf, "w") as f:
        f.write(s)

def findValue(mkf, var):
    varName = var[2:-1]  #converting $(EXAMPLE) to EXAMPLE
    with open(mkf, "r") as f:
        s = f.read()
    x = re.search(r'%s\s*=\s*(.*)' % varName, s)
    if x == None:
        return None
    else:
        return x.group(1)

if __name__ == "__main__":
    mkfList = scanDir("/home/volkov/work/dev/ext/src/GraphicsMagick-1.3.14")
    nr = set()
    for mkf in mkfList:
        nr |= needReplacement(mkf)
        getRidOfMultilines(mkf)
    d = dict()
    for var in nr:
        for mkf in mkfList:
            val = findValue(mkf, var)
            if val != None:
                d[var] = val
    for var in nr:
        if not (var in d):
            print "WARNING: No value for variable %s" % var
    dKeys = d.keys()
    finishKey = False
    for var in dKeys:
        l = re.findall(r'\$\(\S+?\)', d[var])
        l2 = []
        for x in l:
            if x in d:
                l2.append(x)
        while len(l2) > 0:
            for x in l2:
                if x == var:
                    finishKey = True
                    print "WARNING: Recursive variable usage: [%s] = [%s]" % (var, d[var])
                else:
                    if x in d:
#                        print "Replace [%s] with [%s] in [%s] = [%s]" % (x, d[x], var, d[var])
                        d[var] = re.sub(r'%s' % re.escape(x), d[x], d[var])
#                        print "Replace done: [%s] = [%s]" % (var, d[var])
                    else:
                        assert "Can not reach this code!"
            l2 = []
            if not finishKey:
                l = re.findall(r'\$\(\S+?\)', d[var])
                for x in l:
                    if x in d:
                        l2.append(x)
    for mkf in mkfList:
        with open(mkf, "r") as f:
            s = f.read()
        for x in d:
            s = re.sub(r'%s' % re.escape(x), d[x], s)
        with open(mkf, "w") as f:
            f.write(s)
