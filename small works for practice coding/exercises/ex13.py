import random
import string

print("=" * 40)
print("       PASSWORD GENERATOR")
print("=" * 40)

length = int(input("Enter password length: "))

if length < 4:
    print("Password must be at least 4 characters.")
else:
    characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    password = ""

    for i in range(length):
        password += random.choice(characters)

    print("\nGenerated Password:")
    print(password)

    # Password strength
    if length >= 12:
        print("Strength: Strong 💪")
    elif length >= 8:
        print("Strength: Medium 👍")
    else:
        print("Strength: Weak ⚠️")