print("\nGetting assessment ready...\n")

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.data import Dataset
from tensorflow.keras import losses
from tensorflow.keras.layers import Dense, InputLayer, Activation
from tensorflow.keras.models import Sequential

from experta import *
from experta.fact import *

user_data = open("user_data.txt", "w+")
patient_results = open("patient_results.txt", "w+")

""" GET PATIENT SYMPTOMS """

symptom_questionnaire = [
                     '(1/20) Do you have a cough? ',
                     '(2/20) Do you have muscle aches? ',
                     '(3/20) Are you tired? ',
                     '(4/20) Do you have a sore throat? ',
                     '(5/20) Do you have a runny nose? ',
                     '(6/20) Do you have a stuffy nose? ',
                     '(7/20) Do you have a fever? ',
                     '(8/20) Are you nauseated? ',
                     '(9/20) Are you vomiting? ',
                     '(10/20) Do you have diarrhea? ',
                     '(11/20) Do you have shortness of breath? ',
                     '(12/20) Do you have difficulty breathing? ',
                     '(13/20) Are you experiencing a loss of taste? ',
                     '(14/20) Are you experiencing a loss of smell? ',
                     '(15/20) Do you have a itchy nose? ',
                     '(16/20) Do you have itchy eyes? ',
                     '(17/20) Do you have a itchy mouth? ',
                     '(18/20) Do you have an itchy inner ear? ',
                     '(19/20) Are you frequently sneezing? ',
                     '(20/20) Do you have pink eye? '
                    ]

print("\nPlease answer all questions. Enter 'Y' for Yes and 'N' for No.\n")

for question in symptom_questionnaire: 
    res = input(question)
    user_data.write("% s\n" % (res))

user_data.close()

print("\nAssessing your symptoms...\n")

""" CONDITION CLASSIFICATION """

"""### Load and read the data"""

# load user data from text file 

def get_user_data():
  response_file = open('user_data.txt', 'r')
  user_data = []

  while True:
      # Get next line from file
      res = response_file.readline()

      if (res != ''):
          res = res.strip().upper()
          if (res == 'Y'):
            res = 1
          else:
            res = 0
          user_data.append(res)
      else:
          break
  
  response_file.close()

  return user_data

user_data = get_user_data() 
user_data = np.array([user_data])

data = pd.read_csv("mayo_clinic_data.csv")
data.head()

data['TYPE'].unique()

data.columns

data.shape

label_encoder = preprocessing.LabelEncoder()
 
# Encode labels in column 'TYPE'.
data['TYPE']= label_encoder.fit_transform(data['TYPE'])
 
data['TYPE'].unique()

labels = data['TYPE']
labels

data.drop(['TYPE'], axis=1, inplace=True)
features = data
features.head()

"""### Data Split"""

SEED = 100

X = features

# create training and validation sets with 80-20 split
X_train, X_validation, y_train, y_validation = train_test_split(X, labels, test_size=0.2, random_state = SEED)

# split the validation sets to get a holdout dataset (for testing) 50-50 split
X_validation, X_test, y_validation, y_test = train_test_split(X_validation, y_validation, test_size=0.5, random_state = SEED)

"""### Prepare data for training"""

AUTOTUNE = tf.data.AUTOTUNE
BATCH_SIZE = 32
BUFFER_SIZE = 2000

train_numeric_ds = Dataset.from_tensor_slices((X_train, y_train))

train_numeric_ds = train_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# val dataset
val_numeric_ds = Dataset.from_tensor_slices((X_validation, y_validation))
val_numeric_ds = val_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

# test dataset 
test_numeric_ds = Dataset.from_tensor_slices((X_test, y_test))
test_numeric_ds = test_numeric_ds.batch(BATCH_SIZE).shuffle(BUFFER_SIZE).prefetch(AUTOTUNE)

"""### Modelling"""

model = Sequential([
                    InputLayer(input_shape=X_train.shape[1:]),
                    Dense(300, activation='relu'),
                    Dense(100, activation='relu'),
                    Dense(4, activation="softmax") # 4 neurons, 1 per class
                  ]) 

print("\nMaking recommendations...\n")

model.compile(
    loss=losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer='sgd',
    metrics=['accuracy'])

history = model.fit(
    train_numeric_ds, validation_data=val_numeric_ds, epochs=10, verbose=0)

""" Run inference """

"""
A function to find the label with the maximum score.
"""
class_values = tf.constant([0, 1, 2, 3])

def get_label(user_input):
  predicted_scores_batch = model.predict(user_input)
  predicted_int_labels = tf.argmax(predicted_scores_batch, axis=1)
  predicted_labels = tf.gather(class_values, predicted_int_labels)
  return predicted_labels

"""
Now, the model can take user input (symptoms) and predict a score for each label using Model.predict. 
"""
predicted_condition = get_label(user_data)
patient_prediction = predicted_condition[0].numpy()
patient_prediction = patient_prediction.item()

CONDITION = {
    0: "You likely have an allergy. Depending on your allergy, medications can help reduce your immune system reaction and ease symptoms. Your doctor might suggest over-the-counter or prescription medication in the form of pills or liquid, nasal sprays, or eyedrops.\n",
    1: "You likely have a cold. Most people recover from a common cold in three to 10 days, although some colds may last as long as two or three weeks.\n",
    2: "You may have COVID-19. Please get tested immediately and wear a well-fitting mask.\nIf you test positive for COVID-19:\n-Stay home for 5 days.\n-If you have no symptoms or your symptoms are resolving after 5 days, you can leave your house.\n-Continue to wear a mask around others for 5 additional days.\n-If you have a fever, continue to stay home until your fever resolves.",
    3: "You likely have the flu. To avoid infecting other people, stay home from work, school and other public places for at least 24 hours after your fever is gone without the use of fever-reducing medications. Most people feel better within a week of becoming infected with the flu virus. However, coughing may last for another one or two weeks.\n"
}

patient_results.write("%s\n" %(CONDITION[patient_prediction]))

""" RECOMMENDATIONS """

symptoms = ['COUGH', 'MUSCLE_ACHES', 'TIREDNESS', 'SORE_THROAT', 'RUNNY_NOSE', 'STUFFY_NOSE', 'FEVER', 'NAUSEA', 'VOMITING', 'DIARRHEA', 'SHORTNESS_OF_BREATH', 'DIFFICULTY_BREATHING', 'LOSS_OF_TASTE', 'LOSS_OF_SMELL', 'ITCHY_NOSE', 'ITCHY_EYES', 'ITCHY_MOUTH', 'ITCHY_INNER_EAR', 'SNEEZING', 'PINK_EYE']
    
# the user inputs extracted from the text file
user_responses = user_data[0]

user_symptoms = dict(zip(symptoms, user_responses))
# {'COUGH': 0, 'MUSCLE_ACHES': 0, 'TIREDNESS': 0, 'SORE_THROAT': 1, 'RUNNY_NOSE': 0, 'STUFFY_NOSE': 0, 'FEVER': 1, 'NAUSEA': 1, 'VOMITING': 1, 'DIARRHEA': 0, 'SHORTNESS_OF_BREATH': 1, 'DIFFICULTY_BREATHING': 1, 'LOSS_OF_TASTE': 0, 'LOSS_OF_SMELL': 0, 'ITCHY_NOSE': 0, 'ITCHY_EYES': 0, 'ITCHY_MOUTH': 0, 'ITCHY_INNER_EAR': 0, 'SNEEZING': 0, 'PINK_EYE': 0}

class MakeRecommendations(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        yield Fact(fever=user_symptoms['COUGH'])
        yield Fact(muscle_aches=user_symptoms['MUSCLE_ACHES'])
        yield Fact(sore_throat=user_symptoms['SORE_THROAT'])
        yield Fact(runny_nose=user_symptoms['RUNNY_NOSE'])
        yield Fact(stuffy_nose=user_symptoms['STUFFY_NOSE'])
        yield Fact(fever=user_symptoms['FEVER'])
        yield Fact(nausea=user_symptoms['NAUSEA'])
        yield Fact(vomiting=user_symptoms['VOMITING'])
        yield Fact(diarrhea=user_symptoms['DIARRHEA'])
        yield Fact(itchy_nose=user_symptoms['ITCHY_NOSE'])
        yield Fact(itchy_eyes=user_symptoms['ITCHY_EYES'])
        yield Fact(pink_eye=user_symptoms['PINK_EYE'])

    @Rule(Fact(sore_throat=1))
    def match_with_throat(self):
        """
        Match with every `Fact` which:
        * f['SORE_THROAT'] == 1 
        """
        message = "Consider using a cool-air humidifier and trying a saltwater gargle and lozenges.\n"
        patient_results.write("%s\n" %(message))

    @Rule(Fact(pink_eye=1))
    def match_with_pink_eye(self):
        """
        Match with every `Fact` which:
        * f['PINK_EYE'] == 1 
        """
        message = "Pink eye may get better without antibiotic treatment and without causing any complications. It often improves in 2 to 5 days without treatment but can take 2 weeks to go away completely. Your doctor may prescribe an antibiotic, usually given topically as eye drops or ointment.\n"
        patient_results.write("%s\n" %(message))

    @Rule(Fact(itchy_eyes=1))
    def match_with_itchy_eyes(self):
        """
        Match with every `Fact` which:
        * f['ITCHY_EYES'] == 1 
        """
        message = "Frequently use chilled over-the-counter, lubricating eye drops to relieve itchy eyes.\n"
        patient_results.write("%s\n" %(message))

    @Rule(Fact(fever=1))
    def match_with_fever(self):
        """
        Match with every `Fact` which:
        * f['FEVER'] == 1 
        """
        message = "Please drink plenty of fluids. Take acetaminophen (Tylenol, others) or ibuprofen (Advil, Motrin IB, others) to reduce your symptoms. Call the doctor if the fever doesn't respond to the medication, is consistently 103 F (39.4 C) or higher, or lasts longer than three days.\n"
        patient_results.write("%s\n" %(message))

    @Rule(Fact(diarrhea=1))
    def match_with_diarrhea(self):
        """
        Match with every `Fact` which:
        * f['DIARRHEA'] == 1 
        """
        message = "To treat diarrhea:\n-Drink clear liquids during the day to stay hydrated.\n-Try to get about 2-3 liters (8-12 cups) a day.\n-Sip in small amounts between meals instead of while you eat.\n"
        patient_results.write("%s\n" %(message))

    @Rule(Fact(nausea=1))
    def match_with_nausea(self):
        """
        Match with every `Fact` which:
        * f['NAUSEA'] == 1 
        """
        message = "To treat nausea:\n-Drink clear or ice-cold drinks\n-Eat light, bland foods (such as saltine crackers or plain bread)\n-Eat slowly and eat smaller, more frequent meals\n"
        patient_results.write("%s\n" %(message))

    @Rule(Fact(vomiting=1))
    def match_with_vomiting(self):
        """
        Match with every `Fact` which:
        * f['VOMITING'] == 1 
        """
        message = "To treat vomiting:\n-Gradually drink larger amounts of clear liquids\n-Avoid solid food until the vomiting episode has passed\n-Rest\n-Temporarily discontinue all oral medications, which can irritate the stomach and make vomiting worse\n"
        patient_results.write("%s\n" %(message))

    @Rule(OR(Fact(stuffy_nose=1)))
    def match_with_stuffy_nose(self):
        """
        Match with every `Fact` which:
        * f['STUFFY_NOSE'] == 1 
        """
        message = "Consider taking decongestants and using a nasal saline rinse.\n"
        patient_results.write("%s\n" %(message))

engine = MakeRecommendations()
engine.reset()  # Prepare the engine for the execution
engine.run()

patient_results.close()