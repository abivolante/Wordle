import random
import string
from collections import Counter

# Function for checking if letters in the guess word are in the correct word or in the correct position.
def screen(x, correctLetters, correctLetter_counts):
    # Generating the keyboard
    keyboard = list(string.ascii_uppercase)
    keyboard_checks = {}
    for letter in keyboard:
        keyboard_checks.update([(letter, " ")])

    for i in x:
        guessLetters = list(i.upper())
        Checks = []       # Checks is a list containing the strings "/", "*", and "x"
        Checksvalue = []  # Checksvalue is a list of Boolean values that specifies whether the guess letter has been assigned a Check value

        # Defining a dictionary to count the number of occurrences of a letter from the guessletters.
        # We will start counting during comparisons.
        guessLetters_count = {}
        for letter in guessLetters:
            if letter in guessLetters_count.keys():
                pass
            else:
                guessLetters_count.update([(letter, 0)])

        # We go through the guessletters and for each letter, we check if it is in the right position.
        for j in range(0, 5):
            if guessLetters[j] == correctLetters[j]:
                Checks.insert(j, "/")
                guessLetters_count[guessLetters[j]] += 1
                Checksvalue.insert(j, True)
                keyboard_checks.update([(guessLetters[j], "/")])
            else:
                Checksvalue.insert(j, False)

        # We then go through the guessletters and for each letter that is not assigned a check value,
        # we check if it is in the correct word.
        for j in range(0, 5):
            if Checksvalue[j] == True:
                pass
            elif (guessLetters[j] in correctLetters) and (
                guessLetters_count[guessLetters[j]] <= correctLetter_counts[guessLetters[j]]
            ):
                Checks.insert(j, "*")
                guessLetters_count[guessLetters[j]] += 1
                Checksvalue[j] = True
                keyboard_checks.update([(guessLetters[j], "*")])
            else:
                Checks.insert(j, "x")
                # Don't overwrite a better status (e.g. don't downgrade "/" to "x"
                # if this letter was already correctly placed elsewhere in the guess)
                if keyboard_checks[guessLetters[j]] == " ":
                    keyboard_checks.update([(guessLetters[j], "x")])

        print("  ".join(Checks))
        print("  ".join(guessLetters))
        print("\n")
    print("\n_  _  _  _  _ \n" * (6 - len(x)))
    print("  ".join(keyboard))
    print("  ".join(list(keyboard_checks.values())))


def play(y, name):
    while y.lower() == "yes":

        try:
            with open("sgb-words.txt", "r") as f:
                file = f.readlines()
        except OSerror as ex:
            print(f"An error occured: {ex}")

        # Generating a list without the line breaks, normalized to uppercase
        words = [line.strip().upper() for line in file if line.strip()]

        # Generating a random word (fixed off-by-one: valid indices are 0..len(words)-1)
        correctWord = random.choice(words)
        correctLetters = list(correctWord)

        # Counting the number of occurrences of each letter in the correct word
        # (used later to check for duplicate letters)
        correctLetter_counts = Counter(correctLetters)

        Finish = False  # Becomes True when the user guesses correctly, or ends after six tries
        guesses = []    # List of the user's guesses; passed into screen()
        screen(guesses, correctLetters, correctLetter_counts)

        while not Finish and len(guesses) != 6:
            guess = input("input five letter word ").strip().upper()

            #We make a while loop to make sure word is valid (Correct number of letters and is in the list)
            if len(guess) < 5:
                print("not enough letters")
                valid = False
            elif len(guess) >5:
                print("too many letters")
                valid = False
            elif guess not in words:
                print("not in the dictionary")
                valid= False
            else:
                valid= True

            while not valid:
                guess = input("try again ").strip().upper()
                if len(guess) < 5:
                    print("not enough letters")
                elif len(guess) > 5:
                    print("too many letters")
                elif guess not in words:
                    print("not in the dictionary")
                else:
                    valid = True


            # Checking if the guess is a valid word (also normalized to uppercase)
            while guess not in words or len(guess) != 5:
                guess = input("not a word, try again ").strip().upper()

            guesses.append(guess)
            screen(guesses, correctLetters, correctLetter_counts)

            if guess == correctWord:
                Finish = True
                print(f"Congratulations, {name}! You guessed the word.")

        if not Finish:
            print(f"Game over! The correct word is {correctWord}")

        y = input("Would you like to try again? ")


if __name__ == "__main__":
    name = input("Please input your name ")
    print("Welcome to Wordle!")
    print("Instructions:")
    print("Try to guess the five-letter word. You only have six attempts.")
    print("If the letter is correct and in the right position, '/' will appear on top of the letter.")
    print("If the letter is in the word but in the wrong position, '*' will appear on top of the letter.")
    print("If the letter is not in the word at all, 'x' will appear on top of the letter.\n")
    play(input(f"Would you like to start, {name}? [yes/no] "), name)