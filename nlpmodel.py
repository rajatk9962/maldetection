import pandas as pd
import pickle

# Importing the dataset
dataset = pd.read_csv('benign.csv', delimiter = ',', quoting = 3)
corpus = []

#store all the ad data from csv file into corpus
for i in range(0,186):
    review = dataset['Maltext'][i]
    corpus.append(review)

# Creating the Bag of Words model
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values

# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
with open('malclassifier.pkl', 'wb') as fid:
    pickle.dump(classifier, fid) 
pickle.dump(cv, open('count_vect', 'wb'))   
 
#calculating accuracy    
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)

#calculating precision  
from sklearn.metrics import precision_score
precision = precision_score(y_test,y_pred)

#calculating recall
from sklearn.metrics import recall_score
recall = recall_score(y_test,y_pred)

#calculating f1_score
from sklearn.metrics import f1_score
f1=f1_score(y_test,y_pred)