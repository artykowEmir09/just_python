questions = ("🌍 What is the largest planet in our Solar System?",
             "🦒 What is the tallest animal in the world?",
             "💧 What is the chemical symbol for water?",
             "🇫🇷 What is the capital of France?",
             "🐧 Which bird cannot fly?")

options = (("A. Earth ","B. Mars ","C.Jupiter ","D. Venus "),
           ("A. Elephant","B. Giraffe","C. Horse","D. Camel"),
           ("A. O2","B. CO2","C. H2O","D. HO"),
           ("A. Berlin","B. Madrid","C. Rome","D. Paris"),
           ("A. Eagle","B. Penguin","C. Sparrow","D. Parrot"))
answers = ("C","B","C","D","B")
guesses = []
score = 0
question_num = 0

for question in questions:
    print("-------------------------")
    print (question)
    for option in options[question_num]:
        print(option)
    guess = input("Enter (A,B,C,D)").upper()
    guesses.append(guess)
    if guess == answers[question_num]:
        score+=1
        print("CORRECT")
    else:
        print("INCORRECT")
        print(f"{answers[question_num]} is the correct asnwer ")
    question_num +=1
print("-------------------------")
print("       RESULTS           ")
print("-------------------------")
print("answers: ", end = " ")
for answer in answers:
    print(answer, end=" ")
print()
print("guesses: ", end = " ")
for guess in guesses:
    print(guess, end=" ")
print()
score = int(score/len(questions)*100)
print(F"Your score is :{score}%")
print("-------------------------")
print("-------------------------")