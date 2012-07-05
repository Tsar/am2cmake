#!/usr/bin/env python2.7

import os, string, re

targetFileName = 'CMakeLists.txt'

def scanDir(path):
    filesList = []
    fileName = path + "/" + targetFileName
    if os.path.exists(fileName):
        filesList.append(fileName)
    l = os.listdir(path)
    for pth in l:
        fpth = path + "/" + pth
        if os.path.isdir(fpth):
            filesList.extend(scanDir(fpth))
    return filesList

if __name__ == "__main__":
    repl = dict()
    repl['ADD_GCC_PRECOMPILED_HEADER'] = 'ADD_PRECOMPILED_HEADER'

    filesList = scanDir("/home/volkov/work/apsh/src/unsplitted")
    print 'Found %d files named %s' % (len(filesList), targetFileName)
    for oneFile in filesList:
        with open(oneFile, "r") as f:
            s = f.read()
        for x in repl:
            s = re.sub(r'%s' % re.escape(x), repl[x], s, flags = re.IGNORECASE)
        with open(oneFile, "w") as f:
            f.write(s)
        print 'Processed %s' % oneFile
