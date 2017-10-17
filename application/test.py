import re
import sys 
import os
from bs4 import BeautifulSoup
from array import array
from collections import defaultdict
import glob
"""
dict = {'Name': 'Zara', 'Age': 7}

print dict.setdefault('Age', None)
print "Value : %s" %  dict.setdefault('Sex', None)
print dict

tim = '16:30:10'
print tim.split(":")
x  = [1,2,3]
x.append((45,7,34434,333,333))
print x
"""
"""
def splitWord(text):
	splitText = text.split(" ")
	wordList = []
	times = {}
	for n, w in enumerate(splitText):
		if w in times: 
			times[w] += 1
		else:
			times.setdefault(w,0)
		wordList.append((len(wordList),(text.index((w,times[w]), w.lower())))

	return wordList

"""
"""
reload(sys)  
sys.setdefaultencoding("utf-8")  
f=open("beauty.txt",'r')
def readFile(file):
	for line in file:
		#print line
		transferLine = line.decode("utf8")
		xx      =   ur"([\u4e00-\u9fff]+)"  
		pattern =  re.compile(xx)
		newLine = re.search(u"[\u4e00-\u9fff]+",transferLine)
#		newLine = pattern.findall(transferLine)
#		print "\u4e00"
#		print newLine
		print newLine.group()
readFile(f)
"""


def renameFiles(rootDir):
	listDirs = os.walk(rootDir)
	fileList = []
	fileNumber = 1
	for root, dirs, files in listDirs:
		for f in files:
			filesName = os.path.join(root,f)
			os.rename(filesName,root+"/"+str(fileNumber))
			fileNumber = fileNumber + 1
			
		
"""
def traverseFiles(rootDir):
	listDirs = os.walk(rootDir)
	fileList = []
	fileNumber = 1
	for root, dirs, files in listDirs:
		for f in files:
			filesName = os.path.join(root,f)
			fileList.append(filesName)
	print fileList


renameFiles("documents_nytimes")
traverseFiles("documents_nytimes")

"""




"""
f=open("documents_nytimes/Apple Faces Inquiry in China Over App Store Content - The New York Times.htm","r")

def readFile(file):
	soup = BeautifulSoup(file,"lxml")
	print soup.title.string
	pClassText = soup.find_all('p', attrs={'class': 'story-body-text story-content'})
	pClassText_ = unicode.join(u'\n',map(unicode,pClassText))

	soup_pClassText_ = BeautifulSoup(pClassText_ , "lxml")
	print soup_pClassText_.get_text()
	return soup_pClassText_.get_text()

	

readFile(f)
"""
stopWord = [
    'a', 'about', 'above', 'above', 'across', 'after', 'afterwards', 'again',
    'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although',
    'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another',
    'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as',
    'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been',
    'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides',
    'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can',
    'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe',
    'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight',
    'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even',
    'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few',
    'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former',
    'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
    'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here',
    'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him',
    'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc',
    'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last',
    'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me',
    'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly',
    'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never',
    'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not',
    'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
    'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
    'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
    'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she',
    'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some',
    'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere',
    'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their',
    'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby',
    'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
    'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus',
    'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two',
    'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well',
    'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
    'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which',
    'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will',
    'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
    'yourselves', 'the']
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

def creatInvertedIndex(rootDir,stopWordPara):
	
	index = defaultdict(list)
	#listDirs = os.walk(rootDir)
	#listDirs = listdir_nohidden(rootDir)
	#fileList = []
	fileList =listdir_nohidden(rootDir)
	pageId = []
	titleIndex={}
	tf=defaultdict(list)#term frequencies of terms in documents
	df=defaultdict(int)
	numDocuments=0	
	fileNumber = 1


	for filePath in fileList:
		f = open(filePath,"r")
		pageId = re.sub(r'\D', "", filePath)

		soup = BeautifulSoup(f,"lxml")
		pClassText = soup.find_all('p', attrs={'class': 'story-body-text story-content'})
		pClassText_ = unicode.join(u'\n',map(unicode,pClassText))



		soup_pClassText_ = BeautifulSoup(pClassText_ , "lxml")
		textLine = soup_pClassText_.get_text()
		textLine ='\n'.join((soup.title.string,textLine))
		textLine = textLine.lower()
		textLine = re.sub(r'[^a-z0-9]',' ',textLine)
		textLine = textLine.split()
		textLine = [word for word in textLine if word not in stopWordPara]
		termdictPage = {}
		
		for position, term in enumerate(textLine):
			try:
				termdictPage[term][1].append(position)
			except:
				termdictPage[term]=[pageId, array('I',[position])]

		for termpage, postingpage in termdictPage.iteritems():
			index[termpage].append(postingpage)

	return index

		
		#return soup_pClassText_.get_text()

def creatInvertedIndexFile(index):
	f=open("indexDir/indexFile", 'w')
        for term in index.iterkeys():
            postinglist=[]
            for p in index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            print >> f, ''.join((term,'|',';'.join(postinglist)))
            
        f.close()

invertedIndex = creatInvertedIndex("documents_nytimes",stopWord)
creatInvertedIndexFile(invertedIndex)



