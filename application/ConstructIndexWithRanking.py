import re
import sys 
import os
from bs4 import BeautifulSoup
from array import array
from collections import defaultdict
import math
import glob
#This are stop words which can be ignored 
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

#This function is for traversing all unhidden files.
def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

#The main function of create inverted index
def creatInvertedIndex(rootDir,stopWordPara):
	
	index = defaultdict(list)
	fileList =listdir_nohidden(rootDir)
	pageId = []
	titleIndex={}
	tf=defaultdict(list)#term frequencies of terms in documents
	df=defaultdict(int)#document frequencies in all documents
	numDocuments=0	
	fileNumber = 1

#Traverse all files in given directory. Extracting text and title for all files. Create inverted index.
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
		titleIndex[pageId]=soup.title.string.encode('utf-8')
		#Write position, ID of every term into inverted 
		for position, term in enumerate(textLine):
			try:
				termdictPage[term][1].append(position)
			except:
				termdictPage[term]=[pageId, array('I',[position])]
		# Normalize the vector
		norm=0
		for term, posting in termdictPage.iteritems():
		    norm+=len(posting[1])**2
		norm=math.sqrt(norm)	
		#Record the value of term frequencies and document frequencies for caclulate Tf-idf score
		for term, posting in termdictPage.iteritems():
		    tf[term].append('%.4f' % (len(posting[1])/norm))
		    df[term]+=1

		for termpage, postingpage in termdictPage.iteritems():
			index[termpage].append(postingpage)
		numDocuments+=1

	return index,tf,df,numDocuments,titleIndex
#formatting the iverted index and write it into disk
def creatInvertedIndexFile(index,tf,df,nd,ti):
	f=open("indexDir/indexFile", 'w')
	
        print >>f,nd
        nd=float(nd)	
        for term in index.iterkeys():
            postinglist=[]
            for p in index[term]:
                docID=p[0]
                positions=p[1]
                postinglist.append(':'.join([str(docID) ,','.join(map(str,positions))]))
            postingData=';'.join(postinglist)
            tfData=','.join(map(str,tf[term]))
            idfData='%.4f' % (nd/df[term])
            print >> f, '|'.join((term, postingData, tfData, idfData))
            
        f.close()
    #write the name and id of articles for displaying the searching results
	ft=open("indexDir/titleIndexFile",'w')
	for pageid, title in ti.iteritems():
		print >> ft, pageid, title
	ft.close()
#Rename all the original files in the disk
def renameFiles2(list):
	fileNumber=1
	for file in list:
		os.rename(file,"documents_nytimes/"+str(fileNumber))
		fileNumber = fileNumber + 1

renameFiles2(listdir_nohidden("documents_nytimes"))
invertedIndex,termFrequency,documentFrequency,numberOfDocuments,titleIndex = creatInvertedIndex("documents_nytimes",stopWord)
creatInvertedIndexFile(invertedIndex,termFrequency,documentFrequency,numberOfDocuments,titleIndex)



