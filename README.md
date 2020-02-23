# Malvertisement Detector

A malicious advertisement detector in real time using NLP

## Contents

**ads** folder- dataset of ads used for training.

**maltext** folder- 'index.html' file and 'maltext.php' file to display the result, 'cropped_images' file for images detected by the application.

**model** folder- pickle folder 'malclassifier.pkl' in which the trained model is stored, input vector file 'count_vect' .

**templates** folder- 'main.html' page to enter desired url.

**app.py** file- main file to run the application.

**demo.mp4** file- demo recording.

**maldatabase.sql**- sql database to be imported in xampp for storing images

**nlpmodel.py** file- code to train model.

**requirements.txt** file- list of all modules required to run project.

**traindata.csv** file- training set.

## Instructions

1. Download and store all files in single folder.
2. Place 'maltext' folder in htdocs folder in XAMPP.
3. Import 'maldatabase.sql' database in XAMPP.
4. Download all modules required for the project contained in 'requirements.txt' file through command prompt using the command: 'pip install -r requirements.txt'
5. Download Tesseract-OCR [download link for windows: https://github.com/UB-Mannheim/tesseract/wiki] and chrome webdriver [download link: https://chromedriver.chromium.org/downloads] separately.
6. Perform changes listed in **Modifications** section.
7. Run app.py

## Modifications
The app.py code has to be altered in some lines to set paths according to the machine the project is being run on.

1.(Line 19) create a blank folder to store the downloaded images and set its path in 'folderpath'

2.(Line 34) set executable path for Tesseract-OCR

3.(Line 52,147) set executable path for web driver

*NOTE*: Ensure Tesseract and web driver paths are also added as environment variables in system

