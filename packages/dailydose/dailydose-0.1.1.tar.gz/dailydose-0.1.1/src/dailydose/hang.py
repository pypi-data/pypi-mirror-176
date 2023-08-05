from english_words import english_words_lower_alpha_set
import random


def hangman(num_letter):
    if not num_letter.isnumeric():
        print("The function only take positive integers!")
        return "code 1"
    num_letter = int(num_letter)
    if num_letter < 4:
        num_letter = 4
    if num_letter > 10:
        num_letter = 10
    word = ""
    while len(word) != num_letter or not word.isalpha():
        word = random.choice(list(english_words_lower_alpha_set)).lower()
    view = ["\u0332  "] * len(word)
    total_guess = 2*len(word)
    num_guess = total_guess
    correct = 0
    cache = []
    while True:
        num_wrong = total_guess - num_guess
        hang = [" ========="]
        total_height = total_guess - 3 - int((total_guess - 8) / 2)
        rope_length = 1 + int((total_guess - 8) / 2)
        for i in range(0, min(total_height, num_wrong)):
            hang.insert(0, "\t     |")
            num_wrong -= 1
        if num_wrong > 0:
            hang.insert(0, "\t +---+")
            num_wrong -= 1
        index = 1
        for i in range(0, min(rope_length, num_wrong)):
            hang[index] = "\t |   |"
            num_wrong -= 1
            index += 1
        if num_wrong > 0:
            index = 1 + rope_length
            hang[index] = "\t O   |"
            hang[index + 1] = "\t/|\\  |"
            hang[index + 2] = "\t/ \\  |"
        for i in range(len(hang)):
            print(hang[i])
        print("The word is: " + "".join(view))
        if correct == len(word):
            print("Congratulations, the word is " + "".join(word))
            return word
        if num_guess == 0:
            print("The word is " + "".join(word))
            return word
        valid = False
        user_input = ""
        while not valid:
            user_input = input("Guess a letter: ").lower()
            if len(user_input) == 1 and user_input.isalpha():
                if user_input in cache:
                    print("Try another letter!")
                    continue
                valid = True
                cache.append(user_input)
            else:
                print("Input not valid")
        if word.count(user_input) != 0:
            for i in range(len(word)):
                if user_input == word[i].lower():
                    view[i] = "\u0332" + user_input + " "
                    correct += 1
        else:
            num_guess -= 1
        print("\n", end="")