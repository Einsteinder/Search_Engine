import re
import sys 
import os
import glob
from bs4 import BeautifulSoup
from array import array
from collections import defaultdict

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

def renameFiles(rootDir):
	listDirs = os.walk(rootDir)
	fileList = []
	fileNumber = 1
	for root, dirs, files in listDirs:
		for f in files:
			filesName = os.path.join(root,f)
			print filesName
			os.rename(filesName,root+"/"+str(fileNumber))
			fileNumber = fileNumber + 1

def renameFiles2(list):
	fileNumber=1
	for file in list:
		os.rename(file,"documents_nytimes/"+str(fileNumber))
		fileNumber = fileNumber + 1
renameFiles2(listdir_nohidden("documents_nytimes"))
