"""
Mood Assessment Expert System

This a self-administered patient questionnaire used as a screening tool for:
- anxiety based on the GAD-7 (General Anxiety Disorder-7) scale
- depression based on the Major Depression Index
"""

from experta import *
from experta.fact import *

results = open("results.txt", "w+")

gad_questionnaire = [
                     '(1/19) Feeling nervous, anxious, or on edge: ', 
                     '(2/19) Not being able to stop or control worrying: ',
                     '(3/19) Worrying too much about different things: ',
                     '(4/19) Trouble relaxing: ',
                     '(5/19) Being so restless that it is hard to sit still: ',
                     '(6/19) Becoming easily annoyed or irritable: ',
                     '(7/19) Feeling afraid, as if something awful might happen: '
                    ]

mdi_questionnaire = [
                     '(8/19) Have you felt low in spirits or sad? ',
                     '(9/19) Have you lost interest in your daily activities? ',
                     '(10/19) Have you felt lacking in energy and strength? ',
                     '(11/19) Have you felt less self-confident? ',
                     '(12/19) Have you had a bad conscience or feelings of guilt? ',
                     "(13/19) Have you felt that life wasn't worth living? ",
                     '(14/19) Have you had difficulty concentrating, e.g. when reading the newspaper or watching television? ',
                     '(15/19) Have you felt very restless? ',
                     '(16/19) Have you felt subdued or slowed down? ',
                     '(17/19) Have you had trouble sleeping at night? ',
                     '(18/19) Have you suffered from reduced appetite? ',
                     '(19/19) Have you suffered from increased appetite? '
                    ]

class MoodAssessment(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        self.patient_scores = thisdict = {"anxiety_score": -1, "depression_score": -1} 
        self.mdi_first_selection = [] 
        self.mdi_second_selection = [] 
        self.mdi_third_selection = [] 
        yield Fact(anxiety=-1)
        yield Fact(depression=-1)
    
    @Rule()
    def startup(self):
        print("This is an anxiety and depression self-assessment. Please answer all questions.\n")
        print("Over the last two weeks, how often have you been bothered by the following problems?\n")
        print("Please enter numbers only:")
        print("Not at all = 0, Several days = 1, More than half the days = 2, Nearly every day = 3\n")
        for question in gad_questionnaire: 
            res = int(input(question))
            self.patient_scores["anxiety_score"] = self.patient_scores["anxiety_score"] + res
        
        print("\nHow much of the time have you experienced the following?\n")
        print("Please enter numbers only:")
        print("At no time = 0, Some of the time = 1, Slightly less than half the time = 2, Slightly more than half the time = 3, Most of the time = 4, All the time = 5\n")
        for num, q in enumerate(mdi_questionnaire, start=1):
            if (num == 4 or num == 5):
                res = int(input(q))
                self.mdi_first_selection.append(res) 
            elif (num == 8 or num == 9):
                res = int(input(q))
                self.mdi_second_selection.append(res) 
            elif (num == 11 or num == 12):
                res = int(input(q))
                self.mdi_third_selection.append(res) 
            else:
              res = int(input(q)) 
              self.patient_scores["depression_score"] = self.patient_scores["depression_score"] + res

        # update scoring to reflect max of specific mdi symptoms    
        self.patient_scores["depression_score"] = self.patient_scores["depression_score"] + max(self.mdi_first_selection) + max(self.mdi_second_selection) + max(self.mdi_third_selection)  
        # minimize score for rule execution if mdi score over 30
        if (self.patient_scores["depression_score"] > 29):
            self.patient_scores["depression_score"] = 30 

        self.modify(engine.facts[1], anxiety=self.patient_scores["anxiety_score"])
        self.modify(engine.facts[2], depression=self.patient_scores["depression_score"])

    
    # 0–4: minimal anxiety
    @Rule(OR(Fact(anxiety=0), Fact(anxiety=1), Fact(anxiety=2), Fact(anxiety=3), Fact(anxiety=4)))
    def match_with_minimal_anxiety(self):
        assessment = "You may have minimal anxiety."
        results.write("% s\n" % (assessment))

    # 5–9: mild anxiety 
    @Rule(OR(Fact(anxiety=5), Fact(anxiety=6), Fact(anxiety=7), Fact(anxiety=8), Fact(anxiety=9)))
    def match_with_mild_anxiety(self):
        assessment = "You may have mild anxiety."
        results.write("% s\n" % (assessment))

    # 10–14: moderate anxiety 
    @Rule(OR(Fact(anxiety=10), Fact(anxiety=11), Fact(anxiety=12), Fact(anxiety=13), Fact(anxiety=14)))
    def match_with_moderate_anxiety(self):
        assessment = "You may have moderate anxiety."
        results.write("% s\n" % (assessment))

    # 15–21: severe anxiety 
    @Rule(OR(Fact(anxiety=15), Fact(anxiety=16), Fact(anxiety=17), Fact(anxiety=18), Fact(anxiety=19), Fact(anxiety=20), Fact(anxiety=21)))
    def match_with_severe_anxiety(self):
        assessment = "You may have severe anxiety."
        results.write("% s\n" % (assessment))

    # 20-24: mild depression
    @Rule(OR(Fact(depression=20), Fact(depression=21), Fact(depression=22), Fact(depression=23), Fact(depression=24)))
    def match_with_mild_depression(self):
        assessment = "You may have mild depression."
        results.write("% s\n" % (assessment))

    # 25-29: moderate depression
    @Rule(OR(Fact(depression=25), Fact(depression=26), Fact(depression=27), Fact(depression=28), Fact(depression=29)))
    def match_with_moderate_depression(self):
        assessment = "You may have moderate depression."
        results.write("% s\n" % (assessment))

    # 30+: severe depression
    @Rule(OR(Fact(depression=30)))
    def match_with_severe_depression(self):
        assessment = "You may have severe depression."
        results.write("% s\n" % (assessment))


engine = MoodAssessment()
engine.reset()  
engine.run()