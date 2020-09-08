from pandas import DataFrame, read_csv
import pysolr
import tqdm
import json
import pandas as pd
import os
import re
from PDFExtract import PDFExtract


def get_file_list(root, ftype):
    FileList = []
    FileName = []
    for dirPath, dirNames, fileNames in os.walk(root.encode('utf-8')):
        for f in fileNames:
            if f.find(ftype) > -1:
                FileList.append(os.path.join(dirPath, f))
                FileName.append(f.replace(ftype, "".encode('utf-8')))
    if len(FileList) > 0:
        a = zip(FileList, FileName)
        a = sorted(a, key=lambda t: t[1])
        FileList, FileName = zip(*a)
    return list(FileList), list(FileName)


c = 0
author_affliation = {}


def preprocess_author(authors):
    global c
    global author_affliation
    match_object = re.findall(r'[(](.*?)[)]', authors)
    punc1 = '[(](.*?)[)]'
    authors = authors.replace(";", ",")
    authors = authors.replace("*", "")
    authors = re.sub(punc1, '', authors)
    punc2 = 'and'
    authors = re.sub(punc2, ',', authors)
    author = authors.split(',')
    author_list = [a.strip() for a in author if len(a) > 1]
    j = 0
    for i in author_list:
        author_affliation[i] = match_object[j]
        j = j+1
    for i in author_list:
        if i in authors_key.keys():
            pass
        else:
            c = c+1
            authors_key[i] = year+str(c)
    return author_list


if __name__ == '__main__':
    year = input("year: ")
    file_dict={}
    # read Taai Domestic track xlsx data
    df = pd.read_excel("import_xlxs/"+year+"/0.xlsx",keep_default_na=False)
    # read Taai International track xlsx data
    df1 = pd.read_excel("import_xlxs/"+year+"/1.xlsx",keep_default_na=False)
    for i in range(len(df["Paper Title"])):
        if df["Files"][i] and df["Paper Title"][i]:
            filename=df["Files"][i].split(' ')[0]
            file_dict[filename]=df["Paper Title"][i]+".pdf"
    
    for i in range(len(df1["Paper Title"])):
        if df1["Files"][i] and df1["Paper Title"][i]:
            filename=df1["Files"][i].split(' ')[0]
            file_dict[filename]=df1["Paper Title"][i]+".pdf"
    ######### rename filename
    
    PDF_FilePath, PDF_FileName = get_file_list('./pdf/'+year+'/0/',ftype=".pdf".encode('utf-8'))
    PDF_FilePath_2, PDF_FileName_2 = get_file_list('./pdf/'+year+'/1/',ftype=".pdf".encode('utf-8'))
    for i in range(len(PDF_FilePath)):
        filepath,filename=os.path.split(PDF_FilePath[i].decode())
        if file_dict.get(filename,0)!=0:
            os.rename(PDF_FilePath[i], filepath+"/"+file_dict[filename])
    for i in range(len(PDF_FilePath_2)):
        filepath,filename=os.path.split(PDF_FilePath_2[i].decode())
        if file_dict.get(filename,0)!=0:
            os.rename(PDF_FilePath_2[i], filepath+"/"+file_dict[filename])

    ######### covert pdf to text
    PDFExtract_instance = PDFExtract()
    PDFExtract_instance.pdftoText(year)
    # connect the solr server
    server_url = 'http://xxxxx.xxxxx.xxxx'
    solr = pysolr.Solr(server_url, auth=('username', 'password'), timeout=60)
    author_info_solr = pysolr.Solr(
        server_url, auth=('username', 'password'), timeout=60)

    year = str(year)

    authors = {}
    paper_list = []
    authors_key = {}
    with open('authors_key.txt', "r", encoding="utf-8") as json_file:
        authors_key = json.load(json_file)
    FilePath, FileName = get_file_list('./txt/'+year+'/0/',ftype=".txt".encode('utf-8'))
    FilePath_2, FileName_2 = get_file_list('./txt/'+year+'/1/',ftype=".txt".encode('utf-8'))
    content = {}
    for i in range(len(FilePath)):
        with open(FilePath[i], 'r', encoding='utf-8') as f:
            content[FileName[i].decode()] = f.read()
    for i in range(len(FilePath_2)):
        with open(FilePath_2[i], 'r', encoding='utf-8') as f:
            content[FileName_2[i].decode()] = f.read()

    for i in range(len(df["Author Names"])):
        authors[i] = preprocess_author(df["Author Names"][i])

    authors_key_paper = []
    # paper  information
    for i in range(len(df["Paper Title"])):
        if df["Files"][i] or df["Paper Title"][i]:
            continue
        paper = {}
        paper['title'] = df["Paper Title"][i]
        paper['authors'] = authors[i]
        for j in range(len(authors[i])):
            authors_key_paper.append(authors_key[authors[i][j]])
        paper['authors_key'] = authors_key_paper
        authors_key_paper = []
        paper['conference'] = 'Taai Domestic'
        paper['year'] = year
        paper['click'] = 0
        paper['show'] = 0
        paper['abstract'] = df["Abstract"][i]
        paper['content'] = content[paper['title']]
        paper_list.append(paper)

    for i in range(len(df1["Author Names"])):
        authors[i] = preprocess_author(df1["Author Names"][i])

    for i in range(len(df1["Paper Title"])):
        if df1["Files"][i] or df1["Paper Title"][i]:
            continue
        paper = {}
        paper['title'] = df1["Paper Title"][i]
        paper['authors'] = authors[i]
        for j in range(len(authors[i])):
            authors_key_paper.append(authors_key[authors[i][j]])
        paper['authors_key'] = authors_key_paper
        authors_key_paper = []
        paper['conference'] = 'Taai International'
        paper['year'] = year
        paper['click'] = 0
        paper['show'] = 1
        paper['abstract'] = df1["Abstract"][i]
        paper['content'] = content[paper['title']]
        paper_list.append(paper)
    # authers  information
    author_info = {}
    author_info_list = []
    for key in author_affliation.keys():
        if authors_key[key][:4] == year:
            author_info = {}
            author_info['name'] = key
            author_info['key'] = authors_key[key]
            regex = re.compile('^[A-Z][A-Z_a-z\-]+')
            if regex.match(key):
                author_info['english_name'] = key
                author_info['chinese_name'] = ' '
            else:
                author_info['chinese_name'] = key
                author_info['english_name'] = ' '
            author_info['email'] = ' '
            author_info['affiliation'] = author_affliation[key]
            author_info_list.append(author_info)
        else:
            pass

    print("data success")
    # save the authors information  data
    with open('authors_key.txt', 'w', encoding='utf-8') as outfile:
        json.dump(authors_key, outfile)

    # insert all paper information in the search engine
    solr.add(paper_list)
    solr.commit()
    # insert all authors information in the search engine
    author_info_solr.add(author_info_list)
    author_info_solr.commit()
