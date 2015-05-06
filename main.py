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

def main(pathToFile):
    for r, d, f in os.walk(pathToFile):
        for i in f:
            if i.endswith('.avi'):
                print(i)
                
main('C:\\Users\\Lenovo\\Desktop\\downloads')