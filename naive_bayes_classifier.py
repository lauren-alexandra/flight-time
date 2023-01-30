#!/usr/bin/env python3 

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import naive_bayes
from sklearn.model_selection import train_test_split

genre=['Romance','Thriller','Mystery','History','Thriller','Mystery','Mystery','Romance','History','Mystery','History','Romance','Romance','Thriller', 'Romance','Thriller','Mystery','History','Thriller','Mystery','Mystery','Romance','History','Mystery','History','Romance','Romance','Thriller']
cost=['under-5','under-20','under-10','under-30','under-30','under-5','under-20','under-20','under-30','under-10','under-30','under-5','under-5','under-5', 'under-5','under-20','under-10','under-30','under-30','under-5','under-20','under-20','under-30','under-10','under-30','under-5','under-5','under-5']

# labels
buy=['Yes','Yes','No','Yes','Yes','Yes','No','No','Yes','No','Yes','Yes','Yes','Yes','Yes','Yes','No','Yes','Yes','Yes','No','No','Yes','No','Yes','Yes','Yes','Yes']

REC = {
    1: "Buy this book!",
    0: "Don't buy this book."
}
BUY_CLASSES = {
  1: 'Yes',
  0: 'No'
}

# default is 1. Laplacian correction applied later.
ro_no, ro_yes, th_no, th_yes, my_no, my_yes, his_no, his_yes, under_five_no, under_five_yes, under_ten_no, under_ten_yes, under_twenty_no, under_twenty_yes, under_thirty_no, under_thirty_yes = (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

# collect frequency counts 
genre_zip = list(zip(genre, buy))
cost_zip = list(zip(cost, buy))

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
label = labencode.fit_transform(buy)

features = np.transpose((genre, cost))

# split into train and test sets 
X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.3,random_state=32)

# apply Laplacian correction by adding 1 data point for each feature where class probability 0
"""
thriller no
history no
under-5 no
under-30 no
under-10 yes 

2 3 1 0 - 'Romance','Thriller','Mystery','History'
3 1 0 2 - 'under-5','under-20','under-10','under-30'
1 0 - 'Yes', 'No'

[0, 3, 0]  
[2, 2, 0]
[3, 0, 0]
[0, 0, 1]
"""

# add to label
lab_add = [0, 0, 0, 1]
# add to features
feat_add = [[0, 3], [2, 2], [3, 0], [0, 0]]

X_train = np.concatenate((X_train, feat_add), axis=0)
y_train = np.concatenate((y_train, lab_add), axis=0)

model = naive_bayes.GaussianNB()

# train
model.fit(X_train, y_train)

# predict 
book1pred = model.predict([[2,3]]) # 2:Romance, 3:under-5
book1prob = model.predict_proba([[2,3]])
print("\nGiven a book under $5 in the Romance genre:", REC[book1pred[0]])
print("Predicted Value:", BUY_CLASSES[book1pred[0]])
print('Probability for No: ', book1prob[0][0])
print('Probability for Yes: ', book1prob[0][1])

book2pred = model.predict([[3,1]]) # 3:Thriller, 1:under-20
book2prob = model.predict_proba([[3,1]])
print("\nGiven a book under $20 in the Thriller genre:", REC[book2pred[0]])
print("Predicted Value:", BUY_CLASSES[book2pred[0]])
print('Probability for No: ', book2prob[0][0])
print('Probability for Yes: ', book2prob[0][1])

book3pred = model.predict([[0,2]]) # 0:History, 2:under-30
book3prob = model.predict_proba([[2,3]])
print("\nGiven a book under $30 in the History genre:", REC[book3pred[0]])
print("Predicted Value:", BUY_CLASSES[book3pred[0]])
print('Probability for No: ', book3prob[0][0])
print('Probability for Yes: ', book3prob[0][1])

book4pred = model.predict([[1,0]]) # 1:Mystery, 2:under-10
book4prob = model.predict_proba([[1,0]])
print("\nGiven a book under $10 in the Mystery genre:", REC[book4pred[0]])
print("Predicted Value:", BUY_CLASSES[book4pred[0]])
print('Probability for No: ', book4prob[0][0])
print('Probability for Yes: ', book4prob[0][1])

# Calculate the posterior probability by converting the dataset into a frequency table.

# The Frequency table contains the occurrence of labels for all features. 
feat_list = ['Romance','Thriller','Mystery','History', 'under-5','under-10','under-20','under-30']
no_vals = [ro_no, th_no, my_no, his_no, under_five_no, under_ten_no, under_twenty_no, under_thirty_no]
yes_vals = [ro_yes, th_yes, my_yes, his_yes, under_five_yes, under_ten_yes, under_twenty_yes, under_thirty_yes]

freq_table = pd.DataFrame(list(zip(no_vals, yes_vals)), index=feat_list, columns=['No', 'Yes'])
no_total = freq_table['No'].sum()
yes_total = freq_table['Yes'].sum()
freq_table.loc['Total'] = [no_total, yes_total]

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
  
# Posterior Probability for each class
print("\n", freq_table)