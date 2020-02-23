import flask
import pickle
import glob
import pytesseract
import re
import shutil
import os.path
from PIL import Image
from spellchecker import SpellChecker
from sklearn.externals import joblib
from nltk.corpus import stopwords
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import pymysql

# Path to folder where downloaded images are stored

folderpath=r'C:\Users\rajat\Desktop\finalfiles\downloads'

corpus = []
spell = SpellChecker()

#MYSQL connection

db = pymysql.connect("localhost", "root", "", "maldatabase")
cursor = db.cursor()

# Use pickle to load in the pre-trained model
NB_classifier_model = open('model/malclassifier.pkl','rb')
model = joblib.load(NB_classifier_model)

#pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# Initialise the Flask app
app = flask.Flask(__name__, template_folder='templates')

# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('main.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        url = flask.request.form['url']
    
    #open the url provided by user    
    browser = webdriver.Chrome(executable_path=r'C:\Users\rajat\Documents\chromedriver.exe')    
    browser.get(url)
    
    #getting HTML source
    text=browser.page_source
    soup = BeautifulSoup(text, "html.parser")
    
    #find and download all images from website
    imgs = soup.find_all('img')
    links = []
    i=0
    for img in imgs:
        link = img.get ('src')
        if 'https://' not in link:
            link = url + link
        links.append(link)
        #filename= 'img{}.png'.format(i)
        try:
            fullfilename = os.path.join(folderpath, "img_" + str(i) + ".jpg")
            urllib.request.urlretrieve(link,fullfilename )
        except urllib.error.HTTPError as e:
            print(e.code)
            continue
        print ("Image saved for {0}".format(i))
        i+=1
    print('Images detected:' + str(len(links)))
    
    
    #initialize a list images in folder    
    imagenames_list = []   
    
    
    for f in glob.glob(folderpath+'/*.jfif'):
        imagenames_list.append(f)
    for f in glob.glob(folderpath+'/*.jpg'):
        imagenames_list.append(f)
          
            
    for image in imagenames_list:   
        
        #reading the image
        img = Image.open(image)
        
        #ocr
        text = pytesseract.image_to_string(img,lang='eng')
        
        #text filtering
        text=text.replace("\n"," ")
        regex = re.compile('[^a-zA-Z ]')
        text=regex.sub('', text)
        text=re.sub(' +', ' ',text)
        regex1=re.compile(r'\W*\b\w{1,2}\b')
        text=regex1.sub('', text)
        text=text.lower()       
        res=text.split(" ")
        for word in res:
            word=spell.correction(word)
        review = [word for word in res if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        review=review.lstrip()
        
        #append result to a corpus 
        corpus.append(review)
        
            
    
    # Make DataFrame for model
    from sklearn.feature_extraction.text import CountVectorizer
    predicted=[]
    
    #initialize and load vectorizer
    cv = CountVectorizer()
    cv = pickle.load(open('model/count_vect', 'rb'))
    for corps in corpus:
        corps=[corps]
        X = cv.transform(corps).toarray()
        
    # Get the model's prediction
        prediction = model.predict(X)[0]
        if prediction==1:
            predicted.append('malicious')
        else:
            predicted.append('benign')
    combined=[]
    
    #moving images from folder to xampp image folder for frontend
    for i in range(0,len(imagenames_list)):
        combined.append([imagenames_list[i],predicted[i]])
        image_name=os.path.basename(imagenames_list[i])
        predict=predicted[i]
        shutil.move(r"{}".format(imagenames_list[i]),r"C:\xampp\htdocs\maltext\cropped_images\{}".format(image_name))
        cursor.execute(f"INSERT INTO table1(image_name,result) VALUES ('{image_name}','{predict}')")        
        db.commit()
    
    #open frontend displaying all the images    
    browser = webdriver.Chrome(executable_path=r'C:\Users\rajat\Documents\chromedriver.exe')    
    browser.get('http://localhost/maltext/')
    
    
    # Render the form again, but add in the prediction status
    return flask.render_template('main.html',
                                 
                                 result="Detection complete"
                                 )

if __name__ == '__main__':
    app.run()
    
    
    
    
    