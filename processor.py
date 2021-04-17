import re
import pandas as pd
import numpy as np
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
"""
# create stemmer
from pprint import pprint
factory = StemmerFactory()
stemmer = factory.create_stemmer()
"""

stopwords = open("dummy/id.stopwords.02.01.2016.txt").read()
# print(stopwords.split("\n"))
# exit

class BaseIO:
    datas = {
        "csv": None,
        "xls": None,
        "dataframe": None,
    }

    def __init__(self):
        pass
    
    def fromCsv(self, filename):
        pass
    
    def toCsv(self, filename):
        pass
    
    def toXls(self, filename):
        pass
    
    def inputFmt(self, name, filename):
        return {
            "name": name,
            "filename": filename,
        }

class Processor:
    name = "Base processor"
    params = {}
    results = {}
    baseio = None

    def __init__(self, name = "", params = {}):
        # self.name = name
        self.params = params
        self.baseio = BaseIO()
    
    def resultToDict(self):
        for r in self.results.keys():
            self.results[r] = {}

    def addParam(self, key, data):
        self.params[key] = data

        return self

    def setParam(self):
        return self

    def process(self):
        pass
    
    def logs(self, text = ""):
        print(self.name + "::" + text)
        pass

class PreProcessor(Processor):
    name = "Preprocessor"
    results = {
        "crawling": None,
        "preprocess": None,
        "sentimen.y1": None,
        "tfidf": None,
    }
    current = {
        "file": "",
        "index": "",
    }
    preprocesseds = []
    wordsCache = {}
    progress = 0

    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()
    stemmer = None

    def __init__(self, *args, **kwargs):
        super(PreProcessor, self).__init__(*args, **kwargs)
        self.initStemmer()

    def initStemmer(self):
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()

    def crawl(self):
        print("crawling")
    
    def caseFolds(self, sentence):
        pass

    def tokenize(self, text, toWords = False):
        # tokenized = ""
        tokenized = re.sub("[\r\n]"," ", text)
        if toWords:
            tokenized = re.split(r'(\W+)', tokenized)
        else:
            tokenized = re.split(r"[\.\?\!][ \n]", tokenized) # sentences
        tokenized = [t.strip().lower() for t in tokenized if t!="\r"]

        return tokenized
    
    def printProgress(self):
        if self.progress % 100 == 0:
            pref = ["file", str(self.current['file']),"idx", str(self.current['index'])]
            pref = "::".join(pref)
            print("progress::", pref, self.progress)

    def stripLowerAndStem(self, text):
        t = text.strip().lower()
        if self.stemmer:
            return self.stemmer.stem(t)
        
        return t

    """
        1 method 4 all
        # Tokenisasi
        # Data cleaning
        # Case folding
        # Filterisasi atau stopword removal
        # Stemming
    """
    def tokenizeAndClean(self, text, toWords = False):
        # tokenized = ""
        tokenized = re.sub("[\r\n]"," ", text)
        if toWords:
            tokenized = re.split(r'(\W+)', tokenized)
            res = []
            for t in tokenized:
                if t == '':
                    print(t)
                    continue

                lowered = t.lower()

                if lowered in self.wordsCache.keys():
                    res.append(self.wordsCache[lowered])
                    continue

                if t!="\r" and t not in string.punctuation and t not in stopwords and t != '':
                    wordresult = self.stripLowerAndStem(t)
                    res.append(wordresult)
                    self.wordsCache[lowered] = wordresult
                self.progress += 1
                self.current['index'] = self.progress
                self.printProgress()
            # tokenized = [ self.stripLowerAndStem(t) for t in tokenized if t!="\r" and t not in string.punctuation and t not in stopwords and t != '' ]
            ret = res
            # print()
            # exit()
        else:
            tokenized = re.split(r"[\.\?\!][ \n]", tokenized) # sentences
            tokenized = [t.strip().lower() for t in tokenized if t!="\r"]
            ret = tokenized

        return ret

    def preproccess(self):
        print("preproccess")

        crawlResult = self.results['crawling']
        keys = self.results['crawling'].keys()
        for crawled in keys:
            df = crawlResult[crawled]['dataframe']
            dftext = df['text']
            df["preprocessed"] = 1
            print(crawled)
            preprocesseds = []
            
            self.dftext = dftext
            
            print("self.dftext ",len(self.dftext))
            for index, text in enumerate(self.dftext):
                print("text::",index)
                preprocessed = self.tokenizeAndClean(text, True)
                self.preprocesseds.append(preprocessed)
            # for index, row in df.iterrows():
            #     #cleaning
            #     print("text::",index)
            #     self.current['file'] = row
            #     preprocessed = self.tokenizeAndClean(row['text'], True)
            #     self.preprocesseds.append(preprocessed)
            #     preprocesseds.append(preprocessed)
                # if index == 20:
                #     break
            
            # df["preprocessed"] = preprocesseds
            # df["cleaned"] = 1
            # df["caseFolded"] = 1
            # df["stopworded"] = 1
            # df["stemmed"] = 1

            self.results['preprocess']['dataframe'] = df
            # print(df)
            #     self.results['preprocess']["tokenized"]
            # for i, df in enumerate(df):
                # self.tokenize(crawlResult[crawled]['dataframe']['text'])
            # print(crawled)
            # print(crawlResult[crawled]['filename'])
            # print(crawlResult[crawled]['dataframe']['text'])
            # Tokenisasi
            # self.tokenize(crawlResult[crawled]['dataframe']['text'])
            break
        
    
    def classify(self):
        print("classify::inset lexicon")
        self.results["sentimen.y1"] = 1
    
    def tfidfWeighting(self):
        print("classify::tfidfWeighting")
        self.results["tfidf"] = 1

    def process(self):
        pass

class KMeansProcessor(Processor):
    name = "KMeansProcessor"
    results = {
        "cluster.x10": None,
    }

    def __init__(self, *args, **kwargs):
        super(KMeansProcessor, self).__init__(*args, **kwargs)

    def process(self):
        pass

class SVMNBCProcessor(Processor):
    name = "SVMNBCProcessor"
    results = {
        "sentimen.y2": None
    }

    def __init__(self, *args, **kwargs):
        super(SVMNBCProcessor, self).__init__(*args, **kwargs)

    def process(self):
        pass

class RegresiLMProcessor(Processor):
    name = "Regresi"
    results = {
        "sentimen.y2": None
    }

    def __init__(self, *args, **kwargs):
        super(RegresiLMProcessor, self).__init__(*args, **kwargs)

    def process(self):
        pass

baseio = BaseIO()
p = Processor()
preprocessor = PreProcessor()
pKmp = KMeansProcessor()
pSvmnbc = SVMNBCProcessor()
pRegresi = RegresiLMProcessor()

def initialize():
    crawled = [
        baseio.inputFmt("ruu.minol", 'ruu.minol.csv'),
        baseio.inputFmt("ruu.minol2", 'ruu.minol2.csv'),
        baseio.inputFmt("ruu.minuman.beralkohol", 'ruu.minuman.beralkohol.csv'),
        baseio.inputFmt("ruu.minuman.beralkohol2", 'ruu.minuman.beralkohol2.csv'),
        baseio.inputFmt("ruu.miras", 'ruu.miras.csv'),
        baseio.inputFmt("ruu.miras2", 'ruu.miras2.csv'),
    ]

    preprocessor.resultToDict()

    # print(crawled)
    for c in crawled:
        # print(pPre.results['crawling'])
        preprocessor.results['preprocess'][c['name']] = c
        c['dataframe'] = pd.read_csv('./dummy/'+c['filename'], header=0)
        preprocessor.results['crawling'][c['name']] = c
        break


initialize()
preprocessor.preproccess()
# search
"""
df.loc[df['status_id'] == 'x1328208693461196803']
df.loc[df['user_id'] == 'x765149955396734976']['text']
"""
# t1 = 'Pengusul RUU itu kata warga seakan berniat menghapus budaya NTT. Sementara anggota DPRD dari Bali menilai RUU minol bertentangan dengan kebhinekaan Indonesia. https://t.co/97tsrJyj5k https://t.co/natBlBTqAh'
# tz = preprocessor.tokenize(t1, toWords = True)
# tz = preprocessor.tokenize(t1)
# print(tz)

"""
monkey patcher

from processor import *; preprocessor.preproccess();
df = preprocessor.results['crawling']['ruu.minol']['dataframe']; dfp = preprocessor.results['preprocess']['ruu.minol']['dataframe']
"""