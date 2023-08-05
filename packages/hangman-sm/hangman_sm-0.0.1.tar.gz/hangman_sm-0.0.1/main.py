# hangman
import random
from functions import check
from lists import words, another

print("okay, so this is just a simple game of hangman; "
      "the only rule being that you get just seven individual wrong guesses until you lose. "
      "ready? let's go~ ")

word = random.choice(words)

correct = []
incorrect = []
num_correct = 0
guess_or_again = 0

letters = list("_" * len(word))
guess = " "
print(*letters, sep=" ")
print(" ")
again = "yes"

while again == "yes":
    if guess in incorrect or guess in correct:
        guess = input("oops, you already guessed that. enter a different letter: ")
        num_correct = len(correct) - 1
        check(correct, word, guess, letters, incorrect)
    else:
        check(correct, word, guess, letters, incorrect)

    if len(correct) == len(word) or num_correct == len(word):
        again = input("\nyay, you got it! the word was " + word + ". would you like to play again? enter yes or no: ")
        if again == "yes":
            print("\nawesome! here you go:\n")
            word = random.choice(words)

            correct = []
            incorrect = []
            num_correct = 0
            guess_or_again = 0

            letters = list("_" * len(word))
            guess = " "
            print(*letters, sep=" ")
            print(" ")
            again = "yes"
        else:
            break

    elif len(incorrect) == 8:
        again = input("\nah darn, you lose :( the word was " + word +
                      ". would you like to play again? enter yes or no: ")
        if again == "yes":
            print("\nawesome! here you go:\n")
            word = random.choice(words)

            correct = []
            incorrect = []
            num_correct = 0
            guess_or_again = 0

            letters = list("_" * len(word))
            guess = " "
            print(*letters, sep=" ")
            print(" ")
            again = "yes"
        else:
            break

    else:
        if guess_or_again == 0:
            guess = input("guess a letter: ")
            guess_or_again = 1
        else:
            guess = input(random.choice(another))

# ending message
print("i hope you enjoyed to game, and thanks for playing! bye bye :)")
