import random

score = 0
total_questions = 20

print("================================")
print("       MATH QUIZ GAME")
print("================================")

for question in range(1, total_questions + 1):

    num1 = random.randint(1, 200)
    num2 = random.randint(1, 200)

    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        correct_answer = num1 + num2

    elif operation == "-":
        correct_answer = num1 - num2

    else:
        correct_answer = num1 * num2

    print()
    print("Question", question)
    print(num1, operation, num2, "= ?")

    answer = int(input("Your answer: "))

    if answer == correct_answer:
        print("Correct! ✅")
        score += 1
    else:
        print("Wrong! ❌")
        print("Correct answer:", correct_answer)

print()
print("================================")
print("             RESULT")
print("================================")

print("Score:", score, "/", total_questions)

percentage = (score / total_questions) * 100

print("Percentage:", percentage, "%")

if percentage == 100:
    print("Perfect! 🏆")

elif percentage >= 80:
    print("Excellent! 🔥")

elif percentage >= 60:
    print("Good job! 👍")

elif percentage >= 40:
    print("Keep practicing! 💪")

else:
    print("You need more practice. 📚")