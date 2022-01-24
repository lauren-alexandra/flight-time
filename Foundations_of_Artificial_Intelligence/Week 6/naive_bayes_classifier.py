#!/usr/bin/env python3 

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import naive_bayes
from sklearn.model_selection import train_test_split

genre=['Romance','Thriller','Mystery','History','Thriller','Mystery','Mystery','Romance','History','Mystery','History','Romance','Romance','Thriller', 'Romance','Thriller','Mystery','History','Thriller','Mystery','Mystery','Romance','History','Mystery','History','Romance','Romance','Thriller']
cost=['under-5','under-20','under-10','under-30','under-30','under-5','under-20','under-20','under-30','under-10','under-30','under-5','under-5','under-5', 'under-5','under-20','under-10','under-30','under-30','under-5','under-20','under-20','under-30','under-10','under-30','under-5','under-5','under-5']

# labels
read=['Yes','Yes','No','Yes','Yes','Yes','No','No','Yes','No','Yes','Yes','Yes','Yes','Yes','Yes','No','Yes','Yes','Yes','No','No','Yes','No','Yes','Yes','Yes','Yes']

output = {
    1: "Get this book!",
    0: "Don't buy this book."
}

ro_no, ro_yes, th_no, th_yes, my_no, my_yes, his_no, his_yes, under_five_no, under_five_yes, under_ten_no, under_ten_yes, under_twenty_no, under_twenty_yes, under_thirty_no, under_thirty_yes = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

# collect frequency counts 
genre_zip = list(zip(genre, read))
cost_zip = list(zip(cost, read))

for pair in genre_zip:
  if (pair[0] == 'Romance') and (pair[1] == 'Yes'): ro_yes += 1 
  elif (pair[0] == 'Romance') and (pair[1] == 'No'): ro_no += 1 
  elif (pair[0] == 'Thriller') and (pair[1] == 'Yes'): th_yes += 1 
  elif (pair[0] == 'Thriller') and (pair[1] == 'No'): th_no += 1 
  elif (pair[0] == 'Mystery') and (pair[1] == 'Yes'): my_yes += 1 
  elif (pair[0] == 'Mystery') and (pair[1] == 'No'): my_no += 1 
  elif (pair[0] == 'History') and (pair[1] == 'Yes'): his_yes += 1 
  else: his_no += 1   

for pair in cost_zip:
  if (pair[0] == 'under-5') and (pair[1] == 'Yes'): under_five_yes += 1 
  elif (pair[0] == 'under-5') and (pair[1] == 'No'): under_five_no += 1 
  elif (pair[0] == 'under-10') and (pair[1] == 'Yes'): under_ten_yes += 1 
  elif (pair[0] == 'under-10') and (pair[1] == 'No'): under_ten_no += 1 
  elif (pair[0] == 'under-20') and (pair[1] == 'Yes'): under_twenty_yes += 1 
  elif (pair[0] == 'under-20') and (pair[1] == 'No'): under_twenty_no += 1 
  elif (pair[0] == 'under-30') and (pair[1] == 'Yes'): under_thirty_yes += 1 
  else: under_thirty_no += 1

labencode = preprocessing.LabelEncoder()

genre = labencode.fit_transform(genre) 
cost = labencode.fit_transform(cost) 
label = labencode.fit_transform(read)

features = np.transpose((genre, cost))

# split into train and test sets 
X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3,random_state=32)

# apply Laplacian correction by adding 1 data point for each feature-label pair
"""
[0, 3, 1]  
[1, 2, 0]
[2, 1, 0]
[3, 0, 1]
"""

# add to label
lab_add = [1, 0, 0, 1]
# add to features
feat_add = [[0, 3], [1, 2], [2, 1], [3, 0]]

X_train = np.concatenate((X_train, feat_add), axis=0)
y_train = np.concatenate((y_train, lab_add), axis=0)

model = naive_bayes.GaussianNB()

# train
model.fit(X_train, y_train)

# predict 
book1 = model.predict([[2,3]]) # 2:Romance, 3:under-5
book1prob = model.predict_proba([[2,3]])
print("Given a book under $5 in the Romance genre...")
print("Predicted Value:", book1[0])
print(output[book1[0]])

book2 = model.predict([[2,0]]) # 2:Romance, 0:under-10
print("Given a book under $10 in the Romance genre...")
print("Predicted Value:", book2[0])
print(output[book2[0]])

book3 = model.predict([[0,2]]) # 0:History, 2:under-30
print("Given a book under $30 in the History genre...")
print("Predicted Value:", book3[0])
print(output[book3[0]])

book4 = model.predict([[1,0]]) # 1:Mystery, 2:under-10
print("Given a book under $10 in the Mystery genre...")
print("Predicted Value:", book4[0])
print(output[book4[0]])

# Calculate the posterior probability by converting the dataset into a frequency table.

# The Frequency table contains the occurrence of labels for all features. 
feat_list = ['Romance','Thriller','Mystery','History', 'under-5','under-10','under-20','under-30']
no_vals = [ro_no, th_no, my_no, his_no, under_five_no, under_ten_no, under_twenty_no, under_thirty_no]
yes_vals = [ro_yes, th_yes, my_yes, his_yes, under_five_yes, under_ten_yes, under_twenty_yes, under_thirty_yes]

freq_table = pd.DataFrame(list(zip(no_vals, yes_vals)), index=feat_list, columns=['No', 'Yes'])
no_total = freq_table['No'].sum()
yes_total = freq_table['Yes'].sum()
freq_table.loc['Total'] = [no_total, yes_total]
print("Frequency Table")
print(freq_table)

# Likelihood table for the posterior probability
post_prob_no = []
post_prob_yes = []

for num in no_vals:
  post_prob_no.append(num / no_total)

for num in yes_vals:
  post_prob_yes.append(num / yes_total)

post_prob_no.append('')
post_prob_yes.append('')

freq_table['Posterior Probability for No'] = post_prob_no
freq_table['Posterior Probability for Yes'] = post_prob_yes
  
print("Posterior Probability for each class")
print(freq_table)