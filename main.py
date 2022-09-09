import PyPDF2
import os


def pullTextFrompdf(data_dir):
    allfiles =[]
    #iterate through directorry of pdfs
    for files in os.listdir(data_dir):
        if files.endswith(ext):

            # creating a pdf file object 
            pdfFileObj = open(data_dir + '\\' + files, 'rb') 
                
            # creating a pdf reader object 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
                
            # printing number of pages in pdf file 
            print(pdfReader.numPages) 
                
            allpages=[]
            for thispageno in range(0,pdfReader.numPages-1):
                thispage = pdfReader.getPage(thispageno)
                thispagetext = thispage.extract_text()
                print(thispagetext) 
                allpages.append(thispagetext)
            
            allfiles.append(allpages)
            # closing the pdf file object 
            pdfFileObj.close()  
        else:
            continue
    
    return allfiles




thisdir = os.getcwd()

data_dir = thisdir + '\data'
ext = ('.pdf')


allfiles = pullTextFrompdf(data_dir)

x=5
