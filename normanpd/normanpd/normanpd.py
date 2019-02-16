#Code file for normanpd
import urllib.request
import numpy as np
import PyPDF2
from nltk import sent_tokenize
import re
import sqlite3

#Download Data
def fetchincidents(url):
#    temp = tempfile.TemporaryFile()
    
    data = urllib.request.urlopen(url).read()
    # testing
    #f25 = open('/projects/normanpd/2018-02-25 Daily Arrest Summary.pdf',"rb")
    #data = f25.read()
    
    file = open("doc.pdf", 'wb')
    file.write(data)
    file.close()

#    temp.seek(0)
    print("-->Download Complete")

def extractincidents():
    pdfReader = PyPDF2.PdfFileReader('doc.pdf','utf-8')
    no_pgs = pdfReader.getNumPages()

    #Using pdfreader to extract the text
    page = pdfReader.getPage(0).extractText()
    #Gives us back phrases split according to the presence of \n.
    split_lines = page.splitlines()
    #counting the number of rows using;
    row_limit = page.count(';')
    #initializing a list of (row number of) lists
    page_list = [[] for _ in range(row_limit)]
    row_no = 0
    flag = False
    for word in split_lines:
        #looking for the last word in the row
        if not word.endswith(';'):
            page_list[row_no].append(word)
        else:
            #Appending the last word in the row without the ";"
            page_list[row_no].append(word[0:len(word)-1])
            row_no+=1
            if row_no == row_limit: break
#    print(len(page_list))

    head = page_list[0][0:page_list[0].index('Officer')+1]
    page_list[0] = page_list[0][page_list[0].index('Officer')+1:]
    page_list = [head] + page_list
#    print('''page_list,'''"No of rows:",row_limit,len(page_list))
    #Adding the string next to the strings with a space at the end.
    for row_ind, row in enumerate(page_list):
        count = 0
        flag = False
        n_row = []
        for ind, phrase in enumerate(row):
            added = False
            if flag :
                n_row.append(row[ind-1]+phrase)
                flag = False
                added = True
            if phrase.endswith(' ') or phrase.endswith('-'):
                flag = True 
            elif not added:
                n_row.append(phrase)
        page_list[row_ind] = n_row
    #print(page_list,len(page_list))
    #Missing values
    for ind , row in enumerate(page_list):
        #print(ind,"\n1/ ",len(row))
        #Checking if  Pin code is in States plac '''row[8].isdigit()'''e
        if len(row) == 11  and re.match(r'\d{5}',row[8]):
            page_list[ind].insert(8,'NA') #Is np.nan better or just NA?
        elif len(row) == 11 and not re.match(r'\d{5}',row[9]): #chekcing if the10th element is a pin
            page_list[ind].insert(9,'NA')
        elif row[6] == 'HOMELESS' and len(row) == 9:
            for i in range(7,10):page_list[ind].insert(i,'NA')
        #this function only handles when there are 2 rows in the same column
        #For an instance of 3 rows we will be removing the extra element and adding the string to the previous element.This occured in arrest report for 24th Feb 2018.Row 2 and Row 6.
        if len(row) > 12 and row[4][-3:] == 'DUS':
            row[3] = row[3]+'DUS'
            del row[4]
        #print("2/ ",len(row))
    #print(page_list) 
    return_list = []
    for row in page_list:
        s = ','
        return_row = row[0:6] + [s.join(row[6:10])] + row[10:12]
        #print(len(return_row),return_row)
        return_list.append(return_row)
    print("-->Extraction Complete: Returned List. No of rows :",len(page_list)-1)
    return return_list[1:]


def createdb():
    db_path = 'normanpd.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS arrests (
        arrest_time TEXT,
        case_number TEXT,
        arrest_location TEXT,
        offense TEXT,
        arrestee_name TEXT,
        arrestee_birthday TEXT,
        arrestee_address TEXT,
        status TEXT,
        officer TEXT);""")
    conn.commit()
    conn.close()
    print("-->normandb created")

def populatedb(page_list):
    db_path = 'normanpd.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for row in page_list:
        #print("-->Inserted:",row)
        c.execute("INSERT INTO arrests values (?,?,?,?,?,?,?,?,?)",row)
        c.execute("SELECT * FROM arrests")
#    c.executemany("INSERT INTO arrests values (?,?,?,?,?,?,?,?,?)",page_list)
    conn.commit()
    conn.close()
    print("-->Normandb populated")


def status(db):
    db_path = db
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    rows = c.execute("SELECT * FROM arrests")
    page_list = []
    for row in rows:
        a = list(row)
        a = ', '.join(elem for elem in a)
        page_list.append(a)
    print("Number of rows in arrests table:",len(page_list))
    pg5 = 'þ\n'.join(row for row in page_list[0:6])
    print(pg5)
    conn.close()







