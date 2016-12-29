import re
import math
vocabfile=open('test.txt','rb')
vocab=vocabfile.readlines()
vocabfile.close()
from Naivebayes import *
def getwords(doc):
    words=doc.lower()     #lower
    words=re.sub(r'<[^<>]+>',"",words) #tags
    words = re.sub(r'[0-9]+','num', words)  # number
    words = re.sub(r'(http|https)://[^\s]*','httpaddr', words) #urls
    words = re.sub(r'[^\s]+@[^\s]+','emailaddr', words) #email
    words = re.sub(r'[$]+', 'dollar', words)  # dollar
    words = re.sub(r'[^a-zA-Z0-9]', ' ', words)
    words=[x for x in words.split()]
       #    if len(x)>1 and len(x)<20] and (x+'\n') not in vocab[0:40]]
    return set(words);
  #  return dict([(w,1) for w in words]) # Return the unique set of words only
def sampletrain(cl):
    print "training the classifier"
    fileID = open('SPAMTrain.label', 'r')
    DATA = fileID.readlines()
    for i in range(3500):
        row=DATA[i].split()
        cat=row[0]
        filename = row[1]
        ff = 'train/'+ filename
        f = open(ff, 'r')
        if (cat == '1'):
           cl.train(f.read(), 'spam')
        else:
          cl.train(f.read(), 'ham')
def sampletest(cl):
    print "testing the classifier"
    fileID = open('SPAMTrain.label', 'r')
    DATA = fileID.readlines()
    tp=0;
    fn=0
    tn=0
    fp=0
    e=0
    for i in range(3501,4327):
        row=DATA[i].split()
        cat=row[0]
        filename = row[1]
        ff = 'train/'+ filename
        dd=open(ff,'r').read()
        x=cl.classify(dd, 'unknown')
        res="good"
        if x=='spam' and cat=='1':
            tn+=1
        elif x=='ham' and cat=='1':
            fn+=1
            res = "bad"
        elif x == 'spam' and cat == '0':
            fp += 1
            res = "bad"
        elif x == 'ham' and cat == '0':
            tp += 1
        else :
            res = "bad"
            e+=1
        print x,cat,res
    print tn,fn,tp,fp,e
    print 100.0*tn/(tn+fn), 100.0*fn/(tn+fn),100.0*tp/(tp+fp), 100.0*fp/(fp+tp), e
    print "sensitivity = ",100.0*tn/(tn+fp)
    print "specificity = ", 100.0*tp /(tp + fn)
    print "accuracy = ", 100.0 * (tp+tn) / (tp + fn+fp+tn)
    print "unknown = ", 100.0*e/(tp+fn+fp+tn+e)
cl=naivebayes(getwords)
sampletrain(cl)
print cl.cc
cl.setthreshold('spam',1)
cl.setthreshold('ham',1)
#z= cl.fc.keys()
#f=[]
#filew=open('test.txt','wb');
#for x in z:
#    f.append(cl.totalfeature(x))
#ll=[(x,y) for (x,y)in sorted(zip(f,z),reverse=True)]
#for (xx,yy) in ll:
    #filew.write (str(xx)+" "),
 #   filew.write(str(yy)+'\n')
   # filew.write(cl.classify(yy,'unknown'))
    #filew.write('\n')
sampletest(cl)