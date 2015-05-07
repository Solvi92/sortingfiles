from datetime import datetime
from collections import Counter
import itertools as it
import re
import urllib
from urllib import request as req
import json
import csv
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt, pi
import os
import shutil

def sort(path, fileName):
    originalFileName = fileName
    if fileName.endswith('.avi') \
            or fileName.endswith('.mp4') \
            or fileName.endswith('.mkv'):
        fileName = fileName.replace('.avi', ' ')
        fileName = fileName.replace('.rm', ' ')
        fileName = fileName.replace('.srt', ' ')
        fileName = fileName.replace('.mp4', ' ')
        fileName = fileName.replace('.mkv', ' ')
        fileName = fileName.replace('.', ' ')
        fileName = fileName.lower()
        fileName = fileName.replace('sample', ' ')
        fileName = fileName.replace('-', '')
        fileName = fileName.strip()
        fileName = fileName.replace('_',' ')


def sortTv(showName):
    pass

def sortAll():
    homeDir = os.getcwd()
    folderToSort = 'downloads'
    folderToSortFullPath = os.path.join(homeDir, folderToSort)
    recyPath = os.path.join(folderToSortFullPath, '_RecycleBin')
    sortedFilesPath = os.path.join(folderToSortFullPath, '_SortedFiles')

    if not os.path.exists(recyPath):
        os.mkdir(recyPath)
    if not os.path.exists(sortedFilesPath):
        os.mkdir(sortedFilesPath)

    for root, dir, files in os.walk(folderToSortFullPath):
        if root.startswith(sortedFilesPath) or root.startswith(recyPath):
            continue
        for file in files:
            if not file.endswith('.mp4') or file.endswith('.avi') \
                    or file.endswith('.mkv') or file.endswith('.srt') \
                    or file.endswith('.rm'):
                #This should go the the Recycle Bin folder
                shutil.move(os.path.join(root, file), os.path.join(recyPath, file))

    for root, dir, files in os.walk(folderToSortFullPath):
        if root.startswith(sortedFilesPath) or root.startswith(recyPath):
            continue
        print(root)
        for file in files:
                sort(folderToSortFullPath, file)

def main():
    print('###########################################\n'
          '#                                         #\n'
          '#      Welcome to Super Sorter 3000       #\n'
          '#                                         #\n'
          '#      Available function:                #\n'
          '#      Write \'sort\' to sort all files     #\n'
          '#                                         #\n'
          '#      Write the \'File name\'  to          #\n'
          '#      sort after filename                #\n'
          '#                                         #\n'
          '###########################################\n')
    #inp = input('Sort or filename \n')
    inp = 'sort'
    if inp == 'sort':
        sortAll()
    else:
        sort(inp)



main()