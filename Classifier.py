import math
class classifier:
    def __init__(self,getfeatures,filename=None):
        self.fc={}
        self.cc={}
        self.getfeatures=getfeatures
        self.thresholds = {}
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1

    def setthreshold(self, cat, t):
        self.thresholds[cat] = t
    def getthreshold(self, cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]
    def fcount(self, f, cat):
         if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])

         return 0.0
    def totalfeature(self, f):
        totals = sum([self.fcount(f, c) for c in self.categories()])
        return totals
    def catcount(self, cat):
         if cat in self.cc:
                return float(self.cc[cat])

         return 0

    def totalcount(self):
            return sum(self.cc.values())

    def categories(self):
            return self.cc.keys()

    def train(self, item, cat):
        features = self.getfeatures(item)
        for f in features:
             self.incf(f, cat)
        self.incc(cat)

    def fprob(self, f, cat):
        if self.catcount(cat) == 0:
            return 0
        return self.fcount(f, cat) / self.catcount(cat)

    def weightedprob(self, f, cat, prf, weight=3.0, ap=0.5):

         basicprob = prf(f, cat)
         totals = sum([self.fcount(f, c) for c in self.categories()])
         bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
         return bp
    def acceptword(self,word,cat):
        return 1
        x=self.weightedprob(word,cat,self.fprob)
        totals = self.totalfeature(word)
        if x>.01:
            return 1
        else:
            return 0
    def classify(self, item, default=None):
        probs = {}
        max = float('-inf')
        best=default
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max:
              max = probs[cat]
              best = cat
        # Make sure the probability exceeds threshold*next best
        if max==0:
            return default
          #  return self.handlezero(item,default)
        for cat in probs:
            if cat == best:
                continue
            if probs[cat] +math.log10(self.getthreshold(best)) > probs[best]:
                return default
        return best