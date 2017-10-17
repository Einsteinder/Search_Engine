
import sys
import re
invertedIndex = "indexDir/indexFile"
index = {}
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
    if len(lists) == 0:
        return []
    # start intersecting from the smaller list
    lists.sort(key=len)
    return list(reduce(lambda x, y: set(x)& set(y), lists))
    

def getTerms(line):
    line = line.lower()
    # put spaces instead of non-alphanumeric characters
    line = re.sub(r'[^a-z0-9 ]',' ',line) 
    line = line.split()
    line = [x for x in line if x not in stopWord]
    return line
    

def getPostings(terms):
    # all terms in the list are guaranteed to be in the index
    return [ index[term] for term in terms ]


def getDocsFromPostings(postings):
    #no empty list in postings
    return [ [x[0] for x in p] for p in postings ]

def owq(q):
	originalQuery=q
	q=getTerms(q)
	if len(q)==0:
		print ''
		return
	elif len(q)>1:
		ftq(originalQuery)
		return

	#q contains only 1 term 
	q=q[0]
	if q not in index:
		print ''
		return
	else:
		p=index[q]
		p=[x[0] for x in p]
		p=' '.join(map(str,p))  #docid's are integers
		print p


def ftq(q):
	"""Free Text Query"""
	q=getTerms(q)
	if len(q)==0:
		print ''
		return

	li=set()
	for term in q:
		try:
			p=index[term]
			p=[x[0] for x in p]
			li=li|set(p)
		except:
	        #term not in index
			pass

	li=list(li)
	li.sort()
	print ' '.join(map(str,li))

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

	print ' '.join(map(str, phraseDocs))    #prints empty line if no matching docs
        
        
def pqDocs(q):
	""" here q is not the query, it is the list of terms """
	phraseDocs=[]
	length=len(q)
	#first find matching docs
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
def readIndex(indexFile):
	f=open(indexFile, 'r');
	for line in f:
		line=line.rstrip()
		term, postings = line.split('|')    #term='termID', postings='docID1:pos1,pos2;docID2:pos1,pos2'
		postings=postings.split(';')        #postings=['docId1:pos1,pos2','docID2:pos1,pos2']
		postings=[x.split(':') for x in postings] #postings=[['docId1', 'pos1,pos2'], ['docID2', 'pos1,pos2']]
		postings=[[int(x[0]), map(int, x[1].split(','))] for x in postings]   #final postings list  
		index[term]=postings
	f.close()

def queryIndex():

    while True:
        q=sys.stdin.readline()
        if q=='':
            break
        pq(q)
readIndex(invertedIndex)
queryIndex()