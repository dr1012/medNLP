import PyPDF2 
from nltk.tokenize import word_tokenize
from stopwords import stop_word_list
import tqdm
import docx
#from wand.image import Image
#from PIL import Image as PI
#import pyocr
#import pyocr.builders
#import io

def extract(filename):
    file_name_string = filename.split(".")
    file_format = file_name_string[-1]

    text = ""

    if file_format == "pdf":
        text =  pdf_extract(filename)

    elif file_format == "docx":
        text = doc_extract(filename)

    elif file_format == "txt":
        text = text_extract(filename)

    else:
        raise Exception('Not an allowed file type!')

    return simple_parse(text)


def simple_parse(text):

    text = text.lower()
    stop_words = stop_word_list()
    #The word_tokenize() function will break our text phrases into #individual words
    tokens = word_tokenize(text)
    #we'll create a new list which contains punctuation we wish to clean
    punctuations = ['(',')',';',':','[',']',',','.','-','\"','\'','{','}',' - ']
    #We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
    #We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
    keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
    return text, tokens, keywords



def pdf_extract(filename):

    #write a for-loop to open many files -- leave a comment if you'd #like to learn how
   
    


    #open allows you to read the file
    pdfFileObj = open(filename,'rb')
    #The pdfReader variable is a readable object that will be parsed
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #discerning the number of pages will allow us to parse through all #the pages
    num_pages = pdfReader.numPages
    count = 0
    text = ""
    #The while loop will read each page
    
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count +=1
        text += pageObj.extractText()
    #This if statement exists to check if the above library returned #words. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text
    #If the above returns as False, we run the OCR library textract to #convert scanned/image based PDF files into text
    else:
        raise Exception('The system cannot extract text from this file!')
    
    return text
        

def text_extract(filename):
    file = open(filename, 'r') 
    return file.read()   
  


def doc_extract(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


'''

#https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/
def ocr(myfilename):
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[1]
    req_image = []
    final_text = []
    image_pdf = Image(filename=myfilename, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))
    for img in req_image: 
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
        return '\n'.join(final_text)

'''       