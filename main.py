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
folderToSortFullPath = ''
recyPath = ''
sortedFilesPath = ''
duplicatesPath = ''
musicPath = ''
duplicatesCounter = 1
#globals end

def moveTvShow(regex, path, originalFileName):
    global duplicatesCounter
    showName = regex.group(1).title()
    season = regex.group(2)
    showName = showName.strip()
    showFolder = os.path.join(sortedFilesPath, showName)
    if str(season).startswith('0'):
        season = str(season)[1:]
    if os.path.exists(showFolder):
        if not os.path.exists(os.path.join(showFolder, 'Season %s'% season)):
            os.makedirs(os.path.join(sortedFilesPath, showName, 'Season %s'% season))
    else:
        #make a new folder and add the show to it in the right season
        os.makedirs(os.path.join(sortedFilesPath, showName, 'Season %s'% season))
    if os.path.exists(os.path.join(showFolder, 'Season %s'% season, originalFileName)):
    # There are two or more files that are called the same, they are moved to _Duplicates
        if not os.path.exists(duplicatesPath):
            os.mkdir(duplicatesPath)
        if os.path.exists(os.path.join(duplicatesPath, originalFileName)):
            #If there are more then two files, then the file is renamed and moved to _Duplicates
            newname = 'Copy - ' + str(duplicatesCounter) + ' ' + originalFileName
            os.rename(os.path.join(path, originalFileName), os.path.join(path, newname))
            shutil.move(os.path.join(path, newname), duplicatesPath)
            duplicatesCounter += 1
        else:
            shutil.move(os.path.join(path, originalFileName), duplicatesPath)
    else:
        shutil.move(os.path.join(path, originalFileName), os.path.join(showFolder, 'Season %s'% season))

def sort(path, fileName):
    originalFileName = fileName
    if fileName.endswith('.avi') \
            or fileName.endswith('.mp4') \
            or fileName.endswith('.mkv') \
            or fileName.endswith('.srt') \
            or fileName.endswith('rm') \
            or fileName.endswith('mpg') \
            or fileName.endswith('divx') \
            or fileName.endswith('m4v'):
        fileName = fileName.replace('.avi', ' ').replace('.rm', ' ').replace('.mpg', ' ')\
            .replace('.m4v', ' ').replace('.divx', ' ').replace('.srt', ' ').replace('.mp4', ' ')\
            .replace('.mkv', ' ').replace('.', ' ').lower().replace('sample', ' ').replace('-', '')\
            .replace('_',' ').replace('\'', '').strip()
        regex = re.search((r'([\w\s]+)s(\d+)\s*e\d+'), fileName)
        if regex: # TV shows with the regex 'TV Show Name s10 e10'
            moveTvShow(regex, path, originalFileName)
        else:
            regex = re.search((r'([\w\s]+) .*(\d+)x\d+'), fileName)
            if regex:# TV shows with the regex 'TV Show Name [10x10]'
                moveTvShow(regex, path, originalFileName)
            else:
                regex = re.search((r'([\w\s]+)\s+(\d)\d\d\s+'), fileName)
                if regex:# TV shows with the regex 'TV Show Name 666'
                    moveTvShow(regex, path, originalFileName)
                else:
                    regex = re.search((r'([\w\s]+)\s+s(\d+)\s+'), fileName)
                    if regex:# TV shows with the regex 'TV Show Name s10'
                        moveTvShow(regex, path, originalFileName)
                    else:
                        regex = re.search((r'([\w\s]+)\s+season\s*(\w+)\s*episode'), fileName)
                        if regex:# TV shows with the regex 'TV Show Name season 10 episode'
                            moveTvShow(regex, path, originalFileName)

def sortAll():
    #make the recycle bin folder and the music folder
    if not os.path.exists(recyPath):
            os.mkdir(recyPath)
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
                    or file.endswith('.mkv') \
                    or file.endswith('.srt') \
                    or file.endswith('.rm') \
                    or file.endswith('.wmv') \
                    or file.endswith('.py') \
                    or file.endswith('mpg') \
                    or file.endswith('divx') \
                    or file.endswith('m4v'):
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

def moveShowToFolder(originalFileName, path, regex, inp):
    global duplicatesCounter
    showName = inp.title()
    season = regex.group(2)
    showName = showName.strip()
    showFolder = os.path.join(sortedFilesPath, showName)
    if str(season).startswith('0'):
        season = str(season)[1:]
    if os.path.exists(showFolder):
        if not os.path.exists(os.path.join(showFolder, 'Season %s'% season)):
            os.makedirs(os.path.join(sortedFilesPath, showName, 'Season %s'% season))
    else:
        #make a new folder and add the show to it in the right season
        os.makedirs(os.path.join(sortedFilesPath, showName, 'Season %s'% season))
    if os.path.exists(os.path.join(showFolder, 'Season %s'% season, originalFileName)):
    # There are two or more files that are called the same, they are moved to _Duplicates
        if not os.path.exists(duplicatesPath):
            os.mkdir(duplicatesPath)
        if os.path.exists(os.path.join(duplicatesPath, originalFileName)):
            #If there are more then two files, then the file is renamed and moved to _
            newname = 'Copy - ' + str(duplicatesCounter) + ' ' + originalFileName
            os.rename(os.path.join(path, originalFileName), os.path.join(path, newname))
            shutil.move(os.path.join(path, newname), duplicatesPath)
            duplicatesCounter += 1
        else:
            shutil.move(os.path.join(path, originalFileName), duplicatesPath)
    else:
        shutil.move(os.path.join(path, originalFileName), os.path.join(showFolder, 'Season %s'% season))

#No season found, then the show will go to the parent folder of the seasons
def showNoSeason(originalFileName, root, inp):
    global duplicatesCounter
    showName = inp.title()
    showName = showName.strip()
    showFolder = os.path.join(sortedFilesPath, showName)
    path = root
    if not os.path.exists(showFolder):
        os.mkdir(showFolder)
    if os.path.exists(os.path.join(showFolder, originalFileName)):
    # There are two or more files that are called the same, they are moved to _Duplicates
        if not os.path.exists(duplicatesPath):
            os.mkdir(duplicatesPath)
        if os.path.exists(os.path.join(duplicatesPath, originalFileName)):
            #If there are more then two files, then the file is renamed and moved to _Duplicates
            newname = 'Copy - ' + str(duplicatesCounter) + ' ' + originalFileName
            os.rename(os.path.join(path, originalFileName), os.path.join(path, newname))
            shutil.move(os.path.join(path, newname), duplicatesPath)
            duplicatesCounter += 1
        else:
            shutil.move(os.path.join(path, originalFileName), duplicatesPath)
    else:
        shutil.move(os.path.join(path, originalFileName), showFolder)

def sortInp(inp):
    inp = str(inp)
    for root, dir, files in os.walk(folderToSortFullPath):
        if root.startswith(sortedFilesPath) or root.startswith(recyPath) or root.startswith(musicPath)\
                or root.startswith(duplicatesPath):
            continue
        for fileName in files:
            originalFileName = fileName
            if fileName.endswith('.avi') \
                or fileName.endswith('.mp4') \
                or fileName.endswith('.mkv') \
                or fileName.endswith('.srt') \
                or fileName.endswith('rm') \
                or fileName.endswith('mpg') \
                or fileName.endswith('divx') \
                or fileName.endswith('m4v'):
                fileName = fileName.replace('.avi', ' ').replace('.rm', ' ').replace('.mpg', ' ').replace('.m4v', ' ').replace('.divx', ' ').replace('.srt', ' ').replace('.mp4', ' ')\
                    .replace('.mkv', ' ').replace('.', ' ').lower().replace('sample', ' ').replace('-', '')\
                    .replace('_',' ').replace('\'', '').strip()
                inp = inp.lower()
                regex = re.search('.*%s.*'% inp, fileName)
                if regex:
                    if not os.path.exists(os.path.join(sortedFilesPath, inp)):
                        os.mkdir(os.path.join(sortedFilesPath, inp.title()))
                    regex = re.search((r'([\w\s]+)s(\d+)\s*e\d+'), fileName)
                    if regex: # TV shows with the regex 'TV Show Name s10 e10'
                        moveShowToFolder(originalFileName, root, regex, inp)
                    else:
                        regex = re.search((r'([\w\s]+) .*(\d+)x\d+'), fileName)
                        if regex:# TV shows with the regex 'TV Show Name [10x10]'
                            moveShowToFolder(originalFileName, root, regex, inp)
                        else:
                            regex = re.search((r'([\w\s]+)\s+(\d)\d\d\s+'), fileName)
                            if regex:# TV shows with the regex 'TV Show Name 666'
                                moveShowToFolder(originalFileName, root, regex, inp)
                            else:
                                regex = re.search((r'([\w\s]+)\s+s(\d+)\s+'), fileName)
                                if regex:# TV shows with the regex 'TV Show Name s10'
                                    moveShowToFolder(originalFileName, root, regex, inp)
                                else:
                                    regex = re.search((r'([\w\s]+)\s+season\s*(\w+)\s*episode'), fileName)
                                    if regex:# TV shows with the regex 'TV Show Name season 10 episode'
                                        moveShowToFolder(originalFileName, root, regex, inp)
                                    else:
                                        #no season was found for the show so it it will be put in no season but only
                                        #in th season name
                                        showNoSeason(originalFileName, root, inp)

def main():
    print('   ###########################################\n'
          '   #                                         #\n'
          '   #      Welcome to Super Sorter 3000       #\n'
          '   #                                         #\n'
          '   #      Available function:                #\n'
          '   #      Write \'sort\' to sort all files     #\n'
          '   #                                         #\n'
          '   #      Write the \'File name\'  to          #\n'
          '   #      sort after filename                #\n'
          '   #                                         #\n'
          '   ###########################################\n')
	
    #init globals
    global folderToSortFullPath
    global recyPath
    global sortedFilesPath
    global duplicatesPath
    global musicPath

    superSorter = 1
    while superSorter != 0:
        location = input('-> Input the complete path of the folder to sort\n')
        while not os.path.exists(os.path.abspath(location)):
            location = input('-> Must be a valid path, please try again \n')
        folderToSortFullPath = location
        recyPath = os.path.join(folderToSortFullPath, '_RecycleBin')
        sortedFilesPath = os.path.join(folderToSortFullPath, '_SortedFiles')
        duplicatesPath = os.path.join(folderToSortFullPath, '_Duplicates')
        musicPath = os.path.join(folderToSortFullPath, '_Music')

        inp = input('-> Sort or File name ? \n')

        #making _SortedFiles
        if not os.path.exists(sortedFilesPath):
            os.mkdir(sortedFilesPath)

        if inp.lower() == 'sort':
            print('......sorting.......')
            sortAll()
        else:
            print('......sorting.......')
            sortInp(inp)
        rmAllEmptyFolders()
        print('Sorting done')
        superSorter = input('Type 0 if you want to quit or type 1 to continue \n')
        while superSorter != '1' and superSorter != '0':
            superSorter = input('Wrong input please type 0 if you want to quit or type 1 to continue \n')
        superSorter = int(superSorter)
main()