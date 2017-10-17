import re
import sys 
import os
from bs4 import BeautifulSoup
from array import array
from collections import defaultdict
for i in range(1,15):
	f = open("documents_nytimes/"+str(i),"r")

	soup = BeautifulSoup(f,"lxml")

	print soup.title.string