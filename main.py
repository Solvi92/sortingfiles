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
    for r, d, f in os.walk(os.getcwd()):
        for i in f:
            print(r)
            if i.endswith('.mp4') or i.endswith('.avi') or i.endswith('.mkv') or i.endswith('.srt'):
                sortTv(i)


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
    inp = input('Sort or filename \n')
    if inp == 'sort':
        sortAll()
    else:
        sort(inp)



main()