import PyPDF2
import os
import pandas as pd

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io


"""
Script made to ingest pdfs of meeting notes and return the preceding, containing, and succeeding paragraphs of the key term, referenced as
the key_term variable

"""

 #change this for the next search term
key_term = "opposition"



#don't change the following unless you know what you're about
colnames = ["Date","Filename","Pageno","Precedingpara","Containingpara","Succeedingpara","Notes"]

#helper methods precede the main text of the file- if this grows bigger we'll move them into their own file
def pullTextFrompdf(data_dir):
    result_df = pd.DataFrame(columns=colnames)
    allfiles =[]
    #iterate through directorry of pdfs
    holdover = False
    for files in os.listdir(data_dir):
        if files.endswith(ext):

            # creating a pdf file object 
            pdfFileObj = open(data_dir + '\\' + files, 'rb') 
                
            # creating a pdf reader object 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
                
            # printing number of pages in pdf file 
            print(pdfReader.numPages) 
                
            allpages=[]
            thisDate=""
            holdoverframe = pd.DataFrame(columns=colnames)
            
            for thispageno in range(0,pdfReader.numPages-1):
                thispage = pdfReader.getPage(thispageno)
                thispagetext = thispage.extract_text()
                print(thispagetext) 
                allpages.append(thispagetext)
                thisDate = thispagetext[-10:]

                if 'n' in thisDate:
                    thisDate = thisDate.strip('n')
                thisDate = thisDate.strip()
                theseparagraphs = thispagetext.split('. \n')
                if holdover:
                    holdoverframe['Succeedingpara'] = theseparagraphs[0]
                    result_df = pd.concat([result_df,holdoverframe], axis = 0)
                    holdover=False

                for idx,thisparagraph in enumerate(theseparagraphs):
                    if key_term in thisparagraph:
                        try:
                            thisframe = pd.DataFrame([[thisDate,files,thispageno+1,theseparagraphs[idx-1], thisparagraph, theseparagraphs[idx+1],""]],columns=colnames )
                            result_df = pd.concat([result_df,thisframe], axis = 0)
                        except:
                            holdoverframe = pd.DataFrame([[thisDate,files,thispageno+1,theseparagraphs[idx-1], thisparagraph, "","page break"]],columns=colnames )
                            holdover = True
            
            allfiles.append(allpages)
            # closing the pdf file object 
            pdfFileObj.close()  
        else:
            continue
    return allfiles, result_df

def print_raw_text(allfiles):
    with open(r'raw_output.txt', 'w') as fp:
        for idx,file in enumerate(allfiles):
            fp.write("NEW MINUTES  " + str(idx + 1) + "\n\n"  )
            for page in file:
                # write each item on a new line
                fp.write("%s\n" % page)
            fp.write('\n')
    print('Done')


#main part of script
thisdir = os.getcwd()
data_dir = thisdir + '\data'
ext = ('.pdf')

allfiles, result_df = pullTextFrompdf(data_dir)
result_df.to_csv("Output.csv")
print_raw_text(allfiles)


print("Total meeting notes " + str(len(allfiles)))