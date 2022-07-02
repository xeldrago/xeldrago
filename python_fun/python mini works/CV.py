from flask import render_template
from flask import request
import flask
from flask import Flask
import predictor
import imageprocess
import pickle
from sklearn.metrics import classification_report
from sklearn.metrics import plot_confusion_matrix
import scikitplot as skplt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import roc_curve, auc
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import EDA as eda
import seaborn as sns
import matplotlib.pyplot as plt
import shutil
from os.path import isfile, join
from os import listdir
import os
import cv2
import numpy as np
import pandas as pd
from skimage.feature import local_binary_pattern, greycomatrix, greycoprops
from matplotlib import pyplot as plt
%matplotlib inline
def create_empty_df():


df = pd.DataFrame()
df['area'] = None
df['perimeter'] = None
df['red_mean'] = None
df['green_mean'] = None
df['blue_mean'] = None
df['f1'] = None
df['f2'] = None
df['red_std'] = None
df['green_std'] = None
df['blue_std'] = None
df['f4'] = None
df['f5'] = None
df['f6'] = None
df['f7'] = None
df['f8'] = None
df['label'] = None
return df
def feature_extractor(filename):


'''
input params:
filename : path of the file that we want to process

Output params:
l : Feature vector
'''

try:
main_img = cv2.imread(filename)
img = cv2.cvtColor(main_img, cv2.COLOR_BGR2RGB)
except:
return "Invalid"

# Preprocessing


gs = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
blur = cv2.GaussianBlur(gs, (25, 25), 0)
ret_otsu, im_bw_otsu = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
kernel = np.ones((25, 25), np.uint8)
closing = cv2.morphologyEx(im_bw_otsu, cv2.MORPH_CLOSE, kernel)

# Shape features
contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt = contours[0]
M = cv2.moments(cnt)
area = cv2.contourArea(cnt)
if area == 0:
    return "Invalid"
perimeter = cv2.arcLength(cnt, True)

current_frame = main_img
filtered_image = closing/255

# Elementwise Multiplication of range bounded filtered_image with current_frame
current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 0] = np.multiply(
    current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 0], filtered_image)  # B channel
current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 1] = np.multiply(
    current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 1], filtered_image)  # G channel
current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 2] = np.multiply(
    current_frame[0:current_frame.shape[0], 0:current_frame.shape[1], 2], filtered_image)  # R channel

img = current_frame

# Color features
# a higher number in order to see the actual color.
red_channel = img[:, :, 0]
green_channel = img[:, :, 1]  # show the intensities of green channe
blue_channel = img[:, :, 2]

red_mean = np.mean(red_channel)
green_mean = np.mean(green_channel)
blue_mean = np.mean(blue_channel)
# standard deviation for colour feature from the image.
red_std = np.std(red_channel)
green_std = np.std(green_channel)
blue_std = np.std(blue_channel)

# amt.of green color in the image
gr = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
boundaries = [([30, 0, 0], [70, 255, 255])]
for (lower, upper) in boundaries:
mask = cv2.inRange(gr, (36, 0, 0), (70, 255, 255))
ratio_green = cv2.countNonZero(mask)/(img.size/3)
f1 = np.round(ratio_green, 2)
# amt. of non green part of the image
f2 = 1-f1

# Texture features using grey level cooccurance matrix
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
g = greycomatrix(img, [1], [0, np.pi/4, np.pi/2, 3*np.pi/4])

# with the help of glcm find the contrast
contrast = greycoprops(g, 'contrast')
f4 = contrast[0][0]+contrast[0][1]+contrast[0][2]+contrast[0][3]
# [0][3] represent no. of times grey level 3 appears at the right of 0

# with the help of glcm find the dissimilarity
dissimilarity = greycoprops(g, prop='dissimilarity')
f5 = dissimilarity[0][0]+dissimilarity[0][1] + \
    dissimilarity[0][2]+dissimilarity[0][3]

# with the help of glcm find the homogeneity
homogeneity = greycoprops(g, prop='homogeneity')
f6 = homogeneity[0][0]+homogeneity[0][1]+homogeneity[0][2]+homogeneity[0][3]

# with the help of glcm find the energy.
energy = greycoprops(g, prop='energy')
f7 = energy[0][0]+energy[0][1]+energy[0][2]+energy[0][3]

# with the help of glcm find the correlation
correlation = greycoprops(g, prop='correlation')
f8 = correlation[0][0]+correlation[0][1]+correlation[0][2]+correlation[0][3]


l = [area, perimeter, red_mean, green_mean, blue_mean,
     f1, f2, red_std, green_std, blue_std,
     f4, f5, f6, f7, f8]
return l
def process_folder(folderpath, df_f, label_f):


'''
input params:
folderpath : Path of the folder that we want to process
df_f = dataframe for specific disease
label_f : label corresponding to the specific disease

Output params:
df_f = Dataframe consisting processed vectors
'''
imagelist = os.listdir(folderpath)
for image in imagelist:
imagepath = os.path.join(folderpath, image)
im_feature = feature_extractor(imagepath)
if im_feature == "Invalid":
continue
im_feature.append(label_f)
df_f.loc[len(df_f)] = im_feature
if len(df_f) % 500 == 0:
print(len(df_f))

return df_f


def process_plant(folderpaths, labels, savepath):


'''
input params:
folderpaths : List of the folderpaths for specific Plant
labels : List of labels
savepath : Path to export datasheet

Output params:
None
'''
datasheet = create_empty_df()
for i in range(len(folderpaths)):
datasheet = process_folder(folderpaths[i], datasheet, labels[i])

datasheet.to_excel(savepath)

return None
folderpaths = ['/content/drive/MyDrive/Plant Disease Detection /Raw_Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/Apple___healthy',
               '/content/drive/MyDrive/Plant Disease Detection /Raw_Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/Apple___Apple_scab',
               '/content/drive/MyDrive/Plant Disease Detection /Raw_Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/Apple___Black_rot',
               '/content/drive/MyDrive/Plant Disease Detection /Raw_Dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/train/Apple___Cedar_apple_rust'

               ]

labels = [0, 1, 2, 3]
savepath = '/content/drive/MyDrive/Plant Disease Detection /Processed_data&models/Apple/dataset.xlsx'
process_plant(folderpaths, labels, savepath)

5.2. Data Cleaning and Machine Learning Model training and testing
# EDA MOdule importing
shutil.copy('/content/drive/MyDrive/DA_Library/EDA.py', 'EDA.py')
raw_data = eda.readfile(
    '/content/drive/MyDrive/Plant Disease Detection /Processed_data&models/Apple/dataset_apple.xlsx')
raw_data.drop(['Unnamed: 0'], axis=1, inplace=True)
eda.correlation(raw_data)
eda.correlationlist(raw_data)
cleaned_data = raw_data.drop(
    ['green_mean', 'red_std', 'blue_std', 'f5', 'f8', 'f1'], axis=1, inplace=False)
cleaned_data = eda.removenullrows(cleaned_data)

df = cleaned_data.reset_index()
X = df.drop(['index', 'label'], axis=1, inplace=False)
y = df['label']
print(X.shape)
print(y.shape)
k = 5
kf = KFold(n_splits=k, random_state=9, shuffle=True)
model = RandomForestClassifier(
    random_state=50, n_estimators=50, max_samples=0.7)

acc_score = []

for train_index, test_index in kf.split(X):
X_train, X_test = X.iloc[train_index, :], X.iloc[test_index, :]
y_train, y_test = y[train_index], y[test_index]
model = RandomForestClassifier(random_state=50, n_estimators=50, max_sample      s=0.7)
model.fit(X_train, y_train)
pred_values = model.predict(X_test)            # classification
acc = accuracy_score(pred_values, y_test)     # Classification

# acc = model.score(X_test,y_test)                # Regression

acc_score.append(acc)

avg_acc_score = sum(acc_score)/k

print('Score of each fold - {}'.format(acc_score))
print('Avg Score : {}'.format(avg_acc_score))

5.3. Evaluation
!pip install scikit-plot

y_true = y_test
y_probas = model.predict_proba(X_test)
skplt.metrics.plot_roc_curve(y_true, y_probas)
plt.show()
y_pred = model.predict(X_test)
plot_confusion_matrix(model, X_test, y_test, values_format='d',
                      cmap='Blues', display_labels=['0', '1', '2', '3'])

print(classification_report(y_test, y_pred, [0, 1, 2, 3]))
lm = RandomForestClassifier(random_state=50, n_estimators=50, max_samples=0.7)
lm.fit(X, y)
print('Training Score: ', lm.score(X, y))
lm.feature_importances_
filename = '/content/drive/MyDrive/Plant Disease Detection /Processed_data&models/Apple/Results/Applemodel_V1.sav'
pickle.dump(lm, open(filename, 'wb'))

5.4. Inference


def apple_p(feature_vector, model):


processed_vector = np.array(feature_vector).reshape(1, -1)
output = model.predict(processed_vector)
output = int(output)
label_dict = {0: 'Apple___healthy', 1: 'Apple___Apple_scab',
              2: 'Apple___Black_rot', 3: 'Apple___Cedar_apple_rust'}
output = label_dict[output]
return output


def corn_p(feature_vector, model):


processed_vector = np.array(feature_vector).reshape(1, -1)
output = model.predict(processed_vector)
output = int(output)
label_dict = {0: 'Corn_(maize)___healthy',
              1: 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
              2: 'Corn_(maize)__Common_rust',
              3: 'Corn_(maize)___Northern_Leaf_Blight'}
output = label_dict[output]
return output


def grapes_p(feature_vector, model):


processed_vector = np.array(feature_vector).reshape(1, -1)
output = model.predict(processed_vector)
output = int(output)
label_dict = {0: 'Grape___healthy',
              1: 'Grape___Black_rot',
              2: 'Grape___Esca_(Black_Measles)',
              3: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)'}
output = label_dict[output]
return output


def potato_p(feature_vector, model):


processed_vector = np.array(feature_vector).reshape(1, -1)
output = model.predict(processed_vector)
output = int(output)
label_dict = {0: 'Potato___healthy',
              1: 'Potato___Early_blight',
              2: 'Potato___Late_blight'}
output = label_dict[output]
return output


def tomato_p(feature_vector, model):


processed_vector = np.array(feature_vector).reshape(1, -1)
output = model.predict(processed_vector)
output = int(output)
label_dict = {0: 'Tomato___healthy',
              1: 'Tomato___Bacterial_spot',
              2: 'Tomato___Early_blight',
              3: 'Tomato___Late_blight',
              4: 'Tomato___Leaf_Mold',
              5: 'Tomato___Septoria_leaf_spot',
              6: 'Tomato___Spider_mites Two-spotted_spider_mite',
              7: 'Tomato___Target_Spot',
              8: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
              9: 'Tomato___Tomato_mosaic_virus'}
output = label_dict[output]
return output

5.4. API
###############################################################
# Plant disease detection
# API V2
# Version 1.1
# API Main Script
###############################################################

###############################################################
# Importing required Libraries and modules
##############################################################

app = Flask(__name__)

applemodelpath = 'models/Applemodel_V1.sav'
apple_model = pickle.load(open(applemodelpath, 'rb'))

cornmodelpath = 'models/cornmodel_V1.sav'
corn_model = pickle.load(open(cornmodelpath, 'rb'))

grapesmodelpath = 'models/grapesmodel_V1.sav'
grapes_model = pickle.load(open(grapesmodelpath, 'rb'))

potatomodelpath = 'models/potatomodel_V1.sav'
potato_model = pickle.load(open(potatomodelpath, 'rb'))

tomatomodelpath = 'models/Tomatomodel_V1.sav'
tomato_model = pickle.load(open(tomatomodelpath, 'rb'))


@app.route("/")
def home():


version = "1.1"
return render_template('index.html', version1=version)


@app.route("/predict", methods=['GET', 'POST'])
def submit():


imagefile = flask.request.files["data_file"].read()
dname = request.form.get('Name')
dname = str(dname)
response = dname[0]
npimg = np.frombuffer(imagefile, np.uint8)
# convert numpy array to image
img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

f_vector = imageprocess.feature_extractor(img)

if response == 'n':
res = "Please select the appropriate plant from the list"
return '<h1>'+res+'</h1>'

if response == 'a':
p_vector = [f_vector['area'], f_vector['perimeter'], f_vector['red_mean'], f_vector['blue_mean'], f_vector['f2'], f_vector['green_std'],
            f_vector['f4'], f_vector['f6'], f_vector['f7']]

res = predictor.apple_p(p_vector, apple_model)
return '<h1>'+res+'</h1>'

if response == 'c':
p_vector = [f_vector['red_mean'], f_vector['green_mean'], f_vector['blue_mean'], f_vector['f2'], f_vector['red_std'], f_vector['blue_std'],
            f_vector['f7'], f_vector['f8']]

res = predictor.corn_p(p_vector, corn_model)
return '<h1>'+res+'</h1>'

if response == 'g':
p_vector = [f_vector['area'], f_vector['perimeter'], f_vector['red_mean'], f_vector['green_mean'], f_vector['blue_mean'], f_vector['f2'],
            f_vector['red_std'], f_vector['green_std'], f_vector['blue_std'], f_vector['f4'], f_vector['f5'], f_vector['f6'], f_vector['f7'], f_vector['f8']]

res = predictor.grapes_p(p_vector, grapes_model)
return '<h1>'+res+'</h1>'

if response == 'p':
p_vector = [f_vector['area'], f_vector['perimeter'], f_vector['green_mean'], f_vector['blue_mean'], f_vector['f2'], f_vector['red_std'],
            f_vector['green_std'], f_vector['blue_std'], f_vector['f4'], f_vector['f5'], f_vector['f7'], f_vector['f8']]

res = predictor.potato_p(p_vector, potato_model)
return '<h1>'+res+'</h1>'

if response == 't':
del f_vector["f1"]
p_vector = list(f_vector.values())

res = predictor.tomato_p(p_vector, tomato_model)
return '<h1>'+res+'</h1>'

if __name__ == "__main__":
app.run()
