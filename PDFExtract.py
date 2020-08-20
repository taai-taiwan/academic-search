import logging
from tqdm import tqdm
import os
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import codecs
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed



class PDFExtract:
    def extractPdfText(self,filePath='',):
        results = ''

        f = open(filePath, 'rb')
        praser = PDFParser(f)
        doc = PDFDocument()
        praser.set_document(doc)
        doc.set_parser(praser)
        doc.initialize()

        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            for page in doc.get_pages():
                interpreter.process_page(page)
                layout = device.get_result()

                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        results += x.get_text()
        return results


    def preprocess(self,data):

        sent_list_0 = sent_tokenize(data)

        punc = '[\W\d]'

        sent_list_1 = []
        for sent in sent_list_0:
            sent_list_1.append(re.sub(punc, ' ', sent.lower()))

        stop = set(stopwords.words('english'))

        sent_list_2 = []
        for sent in sent_list_1:
            sent_list_2.append([w for w in word_tokenize(
                sent) if w not in stop and len(w) > 1])

        sent_list_3 = []

        for sent in sent_list_2:
            if len(sent) > 1:
                sent_list_3.append(sent)

        return sent_list_3


    def get_file_list(self,root, ftype=".pdf"):
        FileList = []
        FileName = []
        for dirPath, dirNames, fileNames in os.walk(root):
            for f in fileNames:
                if f.find(ftype) > -1:
                    FileList.append(os.path.join(dirPath, f))
                    FileName.append(f.replace(ftype, ""))
        if len(FileList) > 0:
            a = zip(FileList, FileName)
            a = sorted(a, key=lambda t: t[1])
            FileList, FileName = zip(*a)
        return list(FileList), list(FileName)



    def pdftoText(self,year):
        # Taai Domestic track
        FilePath, FileName = self.get_file_list('./pdf/'+str(year)+'/0/') 
        # Taai International track      
        FilePath_2, FileName_2 = self.get_file_list('./pdf/'+str(year)+'/1/')   
        # Taai Special Session track
        FilePath_3, FileName_3 = self.get_file_list('./pdf/'+str(year)+'/2/')  


        logging.getLogger("pdfminer").setLevel(logging.ERROR)

        for i in tqdm(range(len(FilePath))):
            sent_list = self.preprocess(self.extractPdfText(FilePath[i]))
            output = codecs.open('./txt/'+str(year)+'/0/' +
                                FileName[i]+'.txt', 'w', encoding='utf-8')
            for sent in sent_list:
                output.write(' '.join(sent))
        for i in tqdm(range(len(FilePath_2))):
            sent_list = self.preprocess(self.extractPdfText(FilePath_2[i]))
            output = codecs.open('./txt/'+str(year)+'/1/' +
                                FileName_2[i]+'.txt', 'w', encoding='utf-8')
            for sent in sent_list:
                output.write(' '.join(sent))
        for i in tqdm(range(len(FilePath_3))):
            sent_list = self.preprocess(self.extractPdfText(FilePath_3[i]))
            output = codecs.open('./txt/'+str(year)+'/2/' +
                                FileName_3[i]+'.txt', 'w', encoding='utf-8')
            for sent in sent_list:
                output.write(' '.join(sent))
