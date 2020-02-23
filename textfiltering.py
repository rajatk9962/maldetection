# import the necessary packages
import pytesseract
import cv2
import re
import glob
import csv
from nltk.corpus import stopwords
from spellchecker import SpellChecker

#downloading the nltk stopwords list
#import nltk
#nltk.download('stopwords')

corpus = []

#initialize the spell checker
spell = SpellChecker()



with open('malicious.csv', 'w', newline='') as file:
    
    writer = csv.writer(file)
   
    text_list=[]
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
    
    #generate a list of images in a folder
    #specify the target folder
    images = [cv2.imread(file) for file in glob.glob(r"C:\Users\rajat\Desktop\opencv-text-recognition\ads\malicious\*")]
        
    for image in images:
        finallist=[]     
        print("\n")
        
        
            
        #get text from image    
        text = pytesseract.image_to_string(image,lang='eng')
        
        #text filtering
        
        text=text.replace("\n"," ")
        regex = re.compile('[^a-zA-Z ]')        
        text=regex.sub('', text)
        text=re.sub(' +', ' ',text)
        regex1=re.compile(r'\W*\b\w{1,2}\b')
        text=regex1.sub('', text)
        text=text.lower()
        
        #generate a list of keywords
        res=text.split(" ")
        
        #spelling correction
        for word in res:
            word=spell.correction(word)
        review = [word for word in res if not word in set(stopwords.words('english'))]            
        review = ' '.join(review)
        review=review.lstrip()
        print (review)
        
        #writing to csv
        writer.writerow([review])
        
        #storing the resultant text in corpus
        corpus.append(review)

#fitting the text into a sparse matrix        
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
        