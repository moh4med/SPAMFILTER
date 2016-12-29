from Classifier import *
class naivebayes(classifier):
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        p=0
        l=0
        acat='ham'
        if cat=='ham':
            acat='spam'
        for f in features:
            if self.acceptword(f,cat):
                p+=math.log10(self.weightedprob(f,cat,self.fprob))
            #if self.acceptword(f,acat):
             #   l *= self.weightedprob(f, acat, self.fprob)
       # if p+l==0:
        #    return p;
        return p#/(p+l)

    def prob(self, item, cat):
         catprob = self.catcount(cat) / self.totalcount()
         docprob = self.docprob(item, cat)
         return docprob +math.log10(catprob)

    def handlezero(self, item,default):
        features = self.getfeatures(item)
        p = 1.0
        l = 1.0
        acat = 'ham'
        cat='spam'
        catprob = self.catcount(cat) / self.totalcount()
        acatprob = self.catcount(acat) / self.totalcount()
        length=len(features)/2
        for f in item:
            if length<=0:
                break
            if self.acceptword(f, cat):
                p *= self.weightedprob(f, cat, self.fprob)
            if self.acceptword(f, acat):
                l *= self.weightedprob(f, acat, self.fprob)
            length-=1
        if p==0 or l==0:
            return default
        if p*catprob>l*acatprob:
            return cat
        else:
            return acat