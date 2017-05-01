import praw
import sys
import string
from nltk.stem import *

reddit = praw.Reddit(user_agent='SimSubReds',
                     client_id='ZLLdCB1K0e4fLA',
                     client_secret='eVBMIHzTJ50CnuUsbjQcczxCBkA',
                     password='wedungoofed',
                     username='UIUCcs410')

def getComments(subred):
    num = 0
    commentList = []
    docCollection = [[] for i in range(10)]
    for s in reddit.subreddit(subred).top('all'):
        if num >= 10:
            return (commentList, docCollection)
            break
        sub = reddit.submission(id=s)
        sub.comments.replace_more(limit=0)
        for comment in sub.comments.list():
            commentList += (comment.body.rstrip()).split()
            docCollection[num] += (comment.body.rstrip()).split()
        num += 1
    return (commentList, docCollection)

def getStopWords(fileName):
    stopwords = []
    with open(fileName) as f:
        for line in f:
            stopwords.append(line.rstrip())
    return stopwords

def genVocab(comments):
    stemmer = PorterStemmer()
    stop = getStopWords(sys.argv[2])
    translator = str.maketrans('', '', string.punctuation)
    vocab = [com.translate(translator).lower() for com in comments]
    actualVocab = [stemmer.stem(v) for v in vocab if v not in stop]
    return (list(set(actualVocab)) , actualVocab)

def genDoc(docArg):
    stemmer = PorterStemmer()
    stop = getStopWords(sys.argv[2])
    translator = str.maketrans('', '', string.punctuation)
    doc = [word.translate(translator).lower() for word in docArg]
    return [stemmer.stem(word) for word in doc if word not in stop]

def getTopKWordsInVocab(vocabLst, vocabActual, k):
    wordCount = {word: 0 for word in vocabLst}
    for word in vocabLst:
        wordCount[word] = vocabActual.count(word)
    sortedWordCount = sorted(wordCount, key=wordCount.__getitem__, reverse=True)
    for i in range(k):
        print (sortedWordCount[i], wordCount[sortedWordCount[i]])
    return sortedWordCount[:k]

def main():
    if len(sys.argv) != 3:
        print ("Wrong number of arguments, expected: 3, got: {}".format((len(sys.argv)-1)))
        print ("Usage: python3 scraper.py [subreddit name] [stopwords filename]")
        sys.exit()
    comments, docCollection = (getComments(sys.argv[1]))
    vocab, orgVocab = genVocab(comments)
    for i in range(len(docCollection)):
        #print (len(docCollection[i]))
        docCollection[i] = genDoc(docCollection[i])
    #print ("New lengths")
    #for doc in docCollection:
        #print (len(doc))
    top5words = getTopKWordsInVocab(vocab, orgVocab, 5)
    print (top5words)

if __name__ == "__main__": main()