
import sys
import re
from collections import defaultdict
invertedIndex = "indexDir/indexFile"
titleIndexFile = "indexDir/titleIndexFile"
index = {}
titleIndex={}
tf={}      #term frequencies
idf={}  #inverse document frequencies
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
def intersectLists(lists):
    if len(lists)==0:
        return []
    lists.sort(key=len)
    return list(reduce(lambda x,y: set(x)&set(y),lists))
#for calculating similarity of query term and those in documents
def dotProduct(vec1, vec2):
    if len(vec1)!=len(vec2):
        return 0
    return sum([ x*y for x,y in zip(vec1,vec2) ])  
#ranking the searching reasult according to the tf-idf scores 
def rankDocuments(terms, docs):
    #term at a time evaluation
    docVectors=defaultdict(lambda: [0]*len(terms))
    queryVector=[0]*len(terms)
    for termIndex, term in enumerate(terms):
        if term not in index:
            continue
        
        queryVector[termIndex]=idf[term]
        
        for docIndex, (doc, postings) in enumerate(index[term]):
            if doc in docs:
                docVectors[doc][termIndex]=tf[term][docIndex]
                
    #calculate the score of each doc
    docScores=[ [dotProduct(curDocVec, queryVector), doc] for doc, curDocVec in docVectors.iteritems() ]
    docScores.sort(reverse=True)
    resultDocs=[x[1] for x in docScores][:10]
    documentID = resultDocs
    #print document titles and document id's
    resultDocs=[ titleIndex[x] for x in resultDocs ]
    for i in range(len(documentID)):
        print documentID[i],resultDocs[i]

#process text of ducument, eliminating stop words and other non-nubmer non-alphabetic charaters
def getTerms(line):
    line=line.lower()
    line=re.sub(r'[^a-z0-9 ]',' ',line) 
    line=line.split()
    line=[x for x in line if x not in stopWord]
    return line
    
#all terms in the list are guaranteed to be in the index
def getPostings(terms):
 
    return [ index[term] for term in terms ]

#no empty list in postings
def getDocsFromPostings(postings):

    return [ [x[0] for x in p] for p in postings ]

#q contains only 1 word
def owq(q):
	originalQuery=q
	q=getTerms(q)

	q=q[0]
	if q not in index:
		print ''
		return
	else:
		postings=index[q]
		docs=[x[0] for x in postings]
		rankDocuments(q, docs)


def pq(queryTerm):
 	originalQuery=queryTerm
	queryTerm=getTerms(queryTerm)
	if len(queryTerm)==0:
		print ''
		return
	elif len(queryTerm)==1:
		owq(originalQuery)
		return

	phraseDocs=pqDocs(queryTerm)

	rankDocuments(queryTerm, phraseDocs)
        
        
def pqDocs(q):
	""" here q is not the query, it is the list of terms """
	phraseDocs=[]
	length=len(q)
	#find matching docs
	for term in q:
	    if term not in index:
	        #if a term doesn't appear in the index
	        #there can't be any document maching it
	        return []

	postings=getPostings(q)    #all the terms in q are in the index
	docs=getDocsFromPostings(postings)
	#docs are the documents that contain every term in the query
	docs=intersectLists(docs)
	#postings are the postings list of the terms in the documents docs only
	for i in xrange(len(postings)):
	    postings[i]=[x for x in postings[i] if x[0] in docs]


	result=[]
	for i in xrange(len(postings[0])):
		result.append(postings[0][i][0])    #append the docid to the result

	return result

#read main index
def readIndex(indexFile,titleIF):

    f=open(indexFile, 'r');
    #read the number of documents
    numDocuments=int(f.readline().rstrip())
    for line in f:
        line=line.rstrip()
        term, postings, tfL, idfL = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
        postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
        postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
        postings=[ [int(x[0]), map(int, x[1].split(','))] for x in postings ]   #final postings list  
        index[term]=postings
        #read term frequencies
        tfL=tfL.split(',')
        tf[term]=map(float, tfL)
        #read inverse document frequency
        idf[term]=float(idfL)
    f.close()
    
    #read title index
    f=open(titleIF, 'r')
    for line in f:
        pageid, title = line.rstrip().split(' ', 1)
        titleIndex[int(pageid)]=title
    f.close()

def queryIndex():

    while True:
        q=sys.stdin.readline()
        if q=='':
            break
        pq(q)
readIndex(invertedIndex,titleIndexFile)
queryIndex()