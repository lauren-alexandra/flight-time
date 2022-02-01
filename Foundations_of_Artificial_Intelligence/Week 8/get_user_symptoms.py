user_data = open("user_data.txt", "w+")

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

print("Please answer all questions. Enter 'Y' for Yes and 'N' for No.\n")

for question in symptom_questionnaire: 
    res = input(question)
    user_data.write("% s\n" % (res))

print("Assessing your symptoms...\n")