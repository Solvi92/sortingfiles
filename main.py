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
musicPath = os.path.join(folderToSortFullPath, '_Music')
duplicatesCounter = 1
#globals end

def moveTvShow(regex, path, originalFileName):
    global duplicatesCounter
    showName = regex.group(1).title()
    season = regex.group(2)
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
        if os.path.exists(os.path.join(duplicatesPath, originalFileName)):
            #If there are more then two then the file is removed
            os.rename(os.path.join(path, originalFileName), os.path.join(path, originalFileName + str(duplicatesCounter)))
            duplicatesCounter += 1
        else:
            shutil.move(os.path.join(path, originalFileName), duplicatesPath)
    else:
        shutil.move(os.path.join(path, originalFileName), os.path.join(showFolder, 'Season %s'% season))

def sort(path, fileName):
    originalFileName = fileName
    if fileName.endswith('.avi') \
            or fileName.endswith('.mp4') \
            or fileName.endswith('.mkv') :
        fileName = fileName.replace('.avi', ' ').replace('.rm', ' ').replace('.srt', ' ').replace('.mp4', ' ')\
            .replace('.mkv', ' ').replace('.', ' ').lower().replace('sample', ' ').replace('-', '').replace('_',' ').strip()
        regex = re.search((r'([\w\s]+)s(\d+)\s*e\d+'), fileName)
        if regex: # TV shows with the regex 'TV Show Name s10 e10'
            moveTvShow(regex, path, originalFileName)
        else:
            regex = re.search((r'([\w\s]+) .*(\d+)x\d+'), fileName)
            if regex:# TV shows with the regex 'TV Show Name [10x10]'
                moveTvShow(regex, path, originalFileName)
            else:
                regex = re.search((r'([\w\s]+)\s+(\d)\d\d\s+'), fileName)
                if regex:
                    moveTvShow(regex, path, originalFileName)
                else:
                    regex = re.search((r'([\w\s]+)\s+s(\d+)\s*'), fileName)
                    if regex:
                        moveTvShow(regex, path, originalFileName)
                    else:
                        regex = re.search((r'([\w\s]+)\s+season\s*(\w+)\s*episode'), fileName)
                        if regex:
                            moveTvShow(regex, path, originalFileName)
                        else:
                            print('regex did not find anything for the file:', fileName)

def sortAll():
    #making _RecycleBin folder and the _SortedFiles folder and the _Duplicates folder
    if not os.path.exists(recyPath):
        os.mkdir(recyPath)
    if not os.path.exists(sortedFilesPath):
        os.mkdir(sortedFilesPath)
    if not os.path.exists(duplicatesPath):
        os.mkdir(duplicatesPath)
    if not os.path.exists(musicPath):
        os.mkdir(musicPath)
    #putting files we don't want in the _RecycleBin folder
    for root, dir, files in os.walk(folderToSortFullPath):
        #we don't want to sort files that we already sorted
        if root.startswith(sortedFilesPath) or root.startswith(recyPath) \
                or root.startswith(duplicatesPath) \
                or root.startswith(musicPath):
            continue
        for file in files:
            if file.endswith('.mp3'):
                shutil.move(os.path.join(root, file), os.path.join(musicPath, file))
            elif file.endswith('.mp4') or file.endswith('.avi') \
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
        if root.startswith(sortedFilesPath) or root.startswith(recyPath) or root.startswith(musicPath)\
                or root.startswith(duplicatesPath):
            continue
        for file in files:
            sort(root, file)

#Removes all empty Folders
def rmAllEmptyFolders():
    for root, dir, files in os.walk(folderToSortFullPath, topdown=False):
        if root.startswith(sortedFilesPath) or root.startswith(recyPath) or root.startswith(musicPath)\
                or root.startswith(duplicatesPath):
            continue
        else:
            if not os.listdir(root):
                os.rmdir(root)

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
    location = input('-> Input the complete path of the folder to sort \n')
    while not os.path.exists(os.path.abspath(location)):
        location = input('-> Must be a valid path, please try again \n')
    inp = input('-> Sort or File name ? \n')
    if inp.lower() == 'sort':
        sortAll()
    else:
        sortInp(inp)
    rmAllEmptyFolders()
    print('Done')

main()