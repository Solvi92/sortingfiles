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

#globals
homeDir = os.getcwd()
folderToSort = 'downloads'
folderToSortFullPath = os.path.join(homeDir, folderToSort)
recyPath = os.path.join(folderToSortFullPath, '_RecycleBin')
sortedFilesPath = os.path.join(folderToSortFullPath, '_SortedFiles')
duplicatesPath = os.path.join(folderToSortFullPath, '_Duplicates')
#globals end

def sort(path, fileName):
    print('hello from sort')
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
        print('going to find regex')
        print('fileName:', fileName)
        regex = re.search((r'([\w\s]+)s(\d+)\s*e\d+ '), fileName)
        print('regex found', regex)
        if regex:
            showName = regex.group(1)
            season = regex.group(2)
            showName.title()
            showName = showName.strip()
            showFolder = os.path.join(sortedFilesPath, showName)
            if os.path.exists(showFolder):
                if not os.path.exists(os.path.join(showFolder, 'Season %s'% season)):
                    os.makedirs(os.path.join(sortedFilesPath, showName, 'Season %s'% season))
            else:
                #make a new folder and add the show to it in the right season
                os.makedirs(os.path.join(sortedFilesPath, showName, 'Season %s'% season))
            if os.path.exists(os.path.join(showFolder, 'Season %s'% season, originalFileName)):
            # There are two or more files that are called the same they are moved to _Duplicates
                shutil.move(os.path.join(path, originalFileName), duplicatesPath)
            else:
                shutil.move(os.path.join(path, originalFileName), os.path.join(showFolder, 'Season %s'% season))
        else: print('regex did not find anything for the file:', fileName)

def sortTv(showName):
    pass

def sortAll():
    #making _RecycleBin folder and the _SortedFiles folder
    if not os.path.exists(recyPath):
        os.mkdir(recyPath)
    if not os.path.exists(sortedFilesPath):
        os.mkdir(sortedFilesPath)
    if not os.path.exists(duplicatesPath):
        os.mkdir(duplicatesPath)
    #putting files we don't want in the _RecycleBin folder
    for root, dir, files in os.walk(folderToSortFullPath):
        if root.startswith(sortedFilesPath) or root.startswith(recyPath) or root.startswith(duplicatesPath):
            continue
        for file in files:
            if file.endswith('.mp4') or file.endswith('.avi') \
                    or file.endswith('.mkv') or file.endswith('.srt') \
                    or file.endswith('.rm') \
                    or file.endswith('.wmv') \
                    or file.endswith('.py'):
                continue
            else:
                #This goes to the Recycle Bin folder
                shutil.move(os.path.join(root, file), os.path.join(recyPath, file))

    #sorting files we want and putting them in the _SortedFiles folder
    for root, dir, files in os.walk(folderToSortFullPath):
        if root.startswith(sortedFilesPath) or root.startswith(recyPath):
            continue
        for file in files:
            print(file, ': is about to be moved')
            sort(root, file)

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
    print('Done')


main()