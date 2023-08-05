def ind(letter, word):
    return [index for index, char in enumerate(word) if char == letter]


def check(correct, word, guess, letters, incorrect):
    if guess.lower() in word:
        for letter in word:
            if guess.lower() == letter:
                correct += guess
                index = ind(letter, word)
                for char in index:
                    letters[char] = letter
        print(*letters, sep=" ")
    else:
        incorrect.append(guess)


