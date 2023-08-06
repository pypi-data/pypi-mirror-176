
class Association():

    def __init__(self,dataFrame,minSupport=0.5,minConfidence=0.8,maxCount=3) -> None:
        """
        :param dataFrame: pandas data frame include data and name
        :param minSupport: mininum support, default value is 0.5
        :param minConfidence: mininum confidence, default value is 0.8
        :param maxCount: maxinum count of maxinum frequent itemset, default value is 3
        :return: None
        """
        self.name = dataFrame.columns.values
        self.data = dataFrame.values
        self.compressSet = []
        self.compressRatio = 1
        self.rows = len(self.data)
        self.cols = len(self.data[0])
        self.pattern = ['•'] * self.cols
        self.minSupport = round(self.rows * minSupport)
        self.minConfidence = minConfidence
        self.maxCount = maxCount 
        self.freqItems = []
        self.associationRules = {}

    def ptGuide(self):
        """
        pattern tree guide find association rules.
        """        
        self.compress() # compress data set to compress set
        self.frequentItemsets(0,self.cols,self.pattern)
        self.maxFrequentItems()

    def compress(self):
        """
        count same data lines to compress data set
        """
        for row in self.data:
            add = True
            for index,item in enumerate(self.compressSet):
                flag = True
                for i in range(self.cols):
                    if row[i]!=item[i]:
                        flag = False
                        break
                if flag:
                    add = False
                    self.compressSet[index][self.cols] = self.compressSet[index][self.cols]+1
            if add:
                temp = list(row)
                temp.append(1)
                self.compressSet.append(temp)
        self.compressRatio = round(len(self.compressSet) / len(self.data),4)

    def frequentItemsets(self,place,end,pattern,deep=1):
        """
        Generate frequent itemsets
        """
        for pointer in range(place,end):
            pat = pattern.copy()
            counter = {}
            for item in self.compressSet:
                k = -1
                for k in range(self.cols):
                    if pat[k]!='•' and pat[k]!=item[k]:
                        break
                if k == self.cols -1:
                    try:
                        counter[item[pointer]] = counter[item[pointer]] + item[len(item)-1]
                    except:
                        counter[item[pointer]] = item[len(item)-1]
            for key,val in counter.items():
                if val > self.minSupport:
                    pat[pointer] = key
                    temp = {}
                    for k,v in enumerate(pat):
                        if v !='•':
                            temp[k]=v
                    temp['len']=len(temp)
                    temp['cnt']=val
                    self.freqItems.append(temp)
                    self.frequentItemsets(pointer+1,end,pat,deep+1)

    def maxFrequentItems(self):
        """
        Find maxinum frequent items
        """
        index = sorted(range(len(self.freqItems)),key= lambda x: (self.freqItems[x]['len'],self.freqItems[x]['cnt']),reverse=True)
        maxCnt = len(self.freqItems[index[0]])
        count = 0
        for idx in index:
            if len(self.freqItems[idx])==maxCnt and count<self.maxCount:
                count = count + 1
                temp = self.freqItems[idx].copy()
                temp.pop('len')
                temp.pop('cnt')
                self.findRules(self.freqItems[idx],temp)

    def findRules(self,item,subset):
        """
        Find association rules in maxinum frequent itemset
        """
        for key in subset:
            temp = subset.copy()
            temp.pop(key)
            res = {}
            for a in self.freqItems:
                if len(a.items()-temp.items())==2 and len(temp.items()-a.items())==0:
                    res = a.copy()
                    break
            if len(res) > 0:
                self.markRules(item,res,item['cnt']/res['cnt'])
                self.findRules(item,temp)

    def markRules(self,item,subset,confidence):
        """
        Append named association rules into associationRules
        """
        if confidence > self.minConfidence:
            temp = item.copy()
            for key in subset:
                temp.pop(key)
            rule = ""
            for key,val in subset.items():
                if key != 'cnt' and key !='len':
                    rule = rule + str(self.name[key]) + "=" + str(val) + " "
            rule = rule + "=> "
            for key,val in temp.items():
                if key != 'cnt' and key !='len':
                    rule = rule + str(self.name[key]) + "=" + str(val) + " "
            self.associationRules[rule] = round(confidence,4)

    def printRules(self):
        for key,val in self.associationRules.items():
            print(key,val)


