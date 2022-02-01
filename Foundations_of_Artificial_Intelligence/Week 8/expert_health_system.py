from experta import *
from experta.fact import *

# patient_results = open("patient_results.txt", "w+")
# patient_results.write("%s\n" %(patient_prediction))
# patient_results.close()

symptoms = ['COUGH', 'MUSCLE_ACHES', 'TIREDNESS', 'SORE_THROAT', 'RUNNY_NOSE', 'STUFFY_NOSE', 'FEVER', 'NAUSEA', 'VOMITING', 'DIARRHEA', 'SHORTNESS_OF_BREATH', 'DIFFICULTY_BREATHING', 'LOSS_OF_TASTE', 'LOSS_OF_SMELL', 'ITCHY_NOSE', 'ITCHY_EYES', 'ITCHY_MOUTH', 'ITCHY_INNER_EAR', 'SNEEZING', 'PINK_EYE']
    
# this will be the user inputs extracted from the text file. 
user_responses = [0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

user_symptoms = dict(zip(symptoms, user_responses))
# {'COUGH': 0, 'MUSCLE_ACHES': 0, 'TIREDNESS': 0, 'SORE_THROAT': 1, 'RUNNY_NOSE': 0, 'STUFFY_NOSE': 0, 'FEVER': 1, 'NAUSEA': 1, 'VOMITING': 1, 'DIARRHEA': 0, 'SHORTNESS_OF_BREATH': 1, 'DIFFICULTY_BREATHING': 1, 'LOSS_OF_TASTE': 0, 'LOSS_OF_SMELL': 0, 'ITCHY_NOSE': 0, 'ITCHY_EYES': 0, 'ITCHY_MOUTH': 0, 'ITCHY_INNER_EAR': 0, 'SNEEZING': 0, 'PINK_EYE': 0}

patient_prediction = 3 #condition

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
        yield Fact(prediction=patient_prediction)
    
    # ALLERGY
    @Rule(Fact(prediction=0))
    def match_with_cold(self):
        """
        Match with every `Fact` which:
        * f['prediction'] == 0
        """
        print("You likely have an allergy. Depending on your allergy, medications can help reduce your immune system reaction and ease symptoms. Your doctor might suggest over-the-counter or prescription medication in the form of pills or liquid, nasal sprays, or eyedrops.\n")
    
    # COLD
    @Rule(Fact(prediction=1))
    def match_with_cold(self):
        """
        Match with every `Fact` which:
        * f['prediction'] == 1
        """
        print("You likely have a cold. Most people recover from a common cold in three to 10 days, although some colds may last as long as two or three weeks.\n")

    # COVID 
    @Rule(Fact(prediction=2))
    def match_with_cold(self):
        """
        Match with every `Fact` which:
        * f['prediction'] == 2
        """
        print("You may have COVID-19. Please get tested immediately and wear a well-fitting mask.\nIf you test positive for COVID-19:\n-Stay home for 5 days.\n-If you have no symptoms or your symptoms are resolving after 5 days, you can leave your house.\n-Continue to wear a mask around others for 5 additional days.\n-If you have a fever, continue to stay home until your fever resolves.")

    # FLU
    @Rule(Fact(prediction=3))
    def match_with_cold(self):
        """
        Match with every `Fact` which:
        * f['prediction'] == 3
        """
        print("You likely have the flu. To avoid infecting other people, stay home from work, school and other public places for at least 24 hours after your fever is gone without the use of fever-reducing medications. Most people feel better within a week of becoming infected with the flu virus. However, coughing may last for another one or two weeks.\n")
       
    @Rule(Fact(sore_throat=1))
    def match_with_throat(self):
        """
        Match with every `Fact` which:
        * f['SORE_THROAT'] == 1 
        """
        print("Consider using a cool-air humidifier and trying a saltwater gargle and lozenges.\n")

    @Rule(Fact(pink_eye=1))
    def match_with_pink_eye(self):
        """
        Match with every `Fact` which:
        * f['PINK_EYE'] == 1 
        """
        print("Pink eye may get better without antibiotic treatment and without causing any complications. It often improves in 2 to 5 days without treatment but can take 2 weeks to go away completely. Your doctor may prescribe an antibiotic, usually given topically as eye drops or ointment.\n")
    
    @Rule(Fact(itchy_eyes=1))
    def match_with_itchy_eyes(self):
        """
        Match with every `Fact` which:
        * f['ITCHY_EYES'] == 1 
        """
        print("Frequently use chilled over-the-counter, lubricating eye drops to relieve itchy eyes.\n")

    @Rule(Fact(fever=1))
    def match_with_fever(self):
        """
        Match with every `Fact` which:
        * f['FEVER'] == 1 
        """
        print("Please drink plenty of fluids. Take acetaminophen (Tylenol, others) or ibuprofen (Advil, Motrin IB, others) to reduce your symptoms. Call the doctor if the fever doesn't respond to the medication, is consistently 103 F (39.4 C) or higher, or lasts longer than three days.\n")
   
    @Rule(Fact(diarrhea=1))
    def match_with_diarrhea(self):
        """
        Match with every `Fact` which:
        * f['DIARRHEA'] == 1 
        """
        print("To treat diarrhea:\n-Drink clear liquids during the day to stay hydrated.\n-Try to get about 2-3 liters (8-12 cups) a day.\n-Sip in small amounts between meals instead of while you eat.\n")
    
    @Rule(Fact(nausea=1))
    def match_with_nausea(self):
        """
        Match with every `Fact` which:
        * f['NAUSEA'] == 1 
        """
        print("To treat nausea:\n-Drink clear or ice-cold drinks\n-Eat light, bland foods (such as saltine crackers or plain bread)\n-Eat slowly and eat smaller, more frequent meals\n")
    
    @Rule(Fact(vomiting=1))
    def match_with_vomiting(self):
        """
        Match with every `Fact` which:
        * f['VOMITING'] == 1 
        """
        print("To treat vomiting:\n-Gradually drink larger amounts of clear liquids\n-Avoid solid food until the vomiting episode has passed\n-Rest\n-Temporarily discontinue all oral medications, which can irritate the stomach and make vomiting worse\n")
    
    @Rule(OR(Fact(stuffy_nose=1)))
    def match_with_stuffy_nose(self):
        """
        Match with every `Fact` which:
        * f['STUFFY_NOSE'] == 1 
        """
        print("Consider taking decongestants and using a nasal saline rinse.\n")

engine = MakeRecommendations()
engine.reset()  # Prepare the engine for the execution
engine.run()