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

def sort(fileName):
    print(fileName)

def sortTv(showName):
    pass

def sortMovie(movieName):
    pass

def sortAll():
    homeDir = os.getcwd()
    os.mkdir(os.path.join(homeDir, 'downloads', 'RecycleBin'))
    for root, dir, files in os.walk(os.path.join(homeDir, 'downloads')):
        for file in files:
            if file.endswith('.mp4') or file.endswith('.avi') \
                    or file.endswith('.mkv') or file.endswith('.srt') \
                    or file.endswith('.rm'):
                sortTv(file)
            else :
                #This should go the the Recycle Bin folder
                shutil.move(os.path.join(root, file), os.path.join(homeDir,'downloads', 'RecycleBin', file))

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