import random
lowest_num = 1
highest = 100
answer = random.randint(lowest_num , highest)
guesses = 0
is_running = True
print("Python number guessing game ")
print(f"Select a number between{lowest_num} and {highest}") 
while is_running:

    guess = input("Enter your guess: ")

    if guess.isdigit():
        guess = int(guess)
        guesses +=1

        if guess < lowest_num or guess > highest:
            print("That number is out of range  ")
            print(F"Please select a number between {lowest_num} and {highest} ")
        elif guess < answer:
            print("too low! Try again")
        elif guess > answer:
            print("Too high! Try again")
        else:
            print(F"Correct! The answer was {answer}")
            print(f"number of guesses: {guesses}")
            is_running = False
    else:
        print("Invalid guesss")
        print(F"Please select a number between {lowest_num} and {highest} ")
