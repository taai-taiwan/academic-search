# TAAI 
## Licenses
### MIT License
- Copyright &copy; 2020 totoro (https://totoro2345678.github.io/)


## package and environment (reference)
- Python 3.7
- solr 8.3.0
- pandas 1.0.1
- pdfminer3k 1.3.1
- pysolr 3.8.1
- SolrClient 0.3.1
- tqdm 4.41.1

## File Structure
Within the download you'll find the following directories and files:

```
TAAI/
├── README.md
├── solr_import_csv.py
├── PDFExtract.py
├── authors_key.txt
├── managed-schema (reference)
    ├── taai
        ├── managed-schema
    ├── author_info
        ├── managed-schema
├── import_xlxs/
    ├── year(2017)/
        ├── 0.xlsx (domestic paper)
        ├── 1.xlsx (international paper)
├── pdf/
    ├── year(2017)/
        ├── 0(domestic paper.pdf)
            ├── 論文名稱.pdf
        ├── 1(international paper.pdf)
            ├── paper_title.pdf
├── txt/
    ├── year(2017)/
        ├── 0.pdf
            ├── 論文名稱.txt
        ├── 1.pdf
            ├── paper_title.txt

```
## solr core

### paper core Field
![](https://i.imgur.com/fHlFTD9.png)
### authers core Field
![](https://i.imgur.com/L5S8OI4.png)

## solr core schema
附在 managed-schema (reference) 資料夾底下，僅供參考

## execel data
### field 
- Paper Title
- Abstract 
- Author Names
- Track Name
- Files

![](https://i.imgur.com/ZsOSVXP.png)

## Attention ! !
- [論文名稱].pdf  
- execel data --[Paper Title]欄位
```
├── pdf/
    ├── year(2017)/
        ├── 0(domestic paper.pdf)
            ├── [論文名稱].pdf
```
### 上述的[論文名稱]、execel裡的 [Paper Title] 欄位檔案名，如是同一份論文，名稱必須要一樣 ! !

## authors_key.txt
為每個作者建立Key–value，例如{"王小明": "20171" }


## RUN 
```
python solr_import_csv.py
```


## 整個流程
- Step 1. 將所有論文pdf裡的文字提取存成txt檔的形式(PDFExtract.py)
- Step 2. 將資料整理好放進solr(solr_import_csv.py)