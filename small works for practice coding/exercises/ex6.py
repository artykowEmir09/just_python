import random
guesses = 0
lowest_num = 1
highest_num = 100
answer = random.randint(lowest_num,highest_num)
is_running =True
print("Python number guessing game ")
print(f"Select a number between{lowest_num} and {highest_num}") 

while is_running:
    guess = input(f"Enter your guess: ")

    if guess.isdigit():
        guess = int(guess)
        guesses +=1
        if  guess < lowest_num or guess > highest_num :
             print("Number is out of range ")
             print(f"Enter a number between {lowest_num} and {highest_num}")
        elif guess > answer :
            print("Too high! Try again")
        elif guess < answer:
             print("Too Low! Try again")
        else:
            print(f"That is CORRECT the number was {answer}")
            print(f"Number of guesses is {guesses}")
            is_running = False
    else:
        print("Invalid guess")
        print(f"Enter a number between {lowest_num} and {highest_num}")


