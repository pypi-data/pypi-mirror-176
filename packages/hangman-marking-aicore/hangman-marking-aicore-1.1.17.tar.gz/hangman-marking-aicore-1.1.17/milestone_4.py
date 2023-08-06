# import random

# class Hangman:
#     def __init__(self, num_lives, word_list):
#         self.word_list = word_list
#         self.num_lives = num_lives
#         self.word = random.choice(word_list)
#         self.word_guessed = ['_' for _ in range(len(self.word))]
#         self.num_letters = len(set(self.word))
#         self.list_of_guesses = []

#     def check_guess(self, guess):
#         if guess in self.word:
#             print(f"Good guess! {guess} is in the word.")
#             for index, letter in enumerate(self.word):
#                 if letter == guess:
#                     self.word_guessed[index] = letter
#             self.num_letters -= 1
#         else:
#             print(f"Sorry, {guess} is not in the word.")
#             self.num_lives -= 1
#             print(f"You have {self.num_lives} lives left.")
    
#     def ask_for_input(self):
#         while True:
#             guess = input("Enter a letter: ")
#             if len(guess) != 1 or not guess.isalpha():
#                 print("Invalid letter. Please, enter a single alphabetical character.")
#             elif guess in self.list_of_guesses:
#                 print("You already tried that letter!")
#             else:
#                 self.check_guess(guess)
#                 self.list_of_guesses.append(guess)
#                 # break
    
        
import random

class Hangman():

    def __init__(self, word_list, num_lives = 5):
        self.word_list = word_list
        self.num_lives = num_lives
        self.word = random.choice(self.word_list)
        self.word_guessed = ['_']*len(self.word)
        self.num_letters = len(set(self.word))
        self.list_of_guesses = []

    def check_guess(self, guess):
        guess = guess.lower()
        if guess in self.word:
            print("Good guess!", guess ,"is in the word.")
            for i in range(len(self.word)):
                if self.word[i] == guess:
                    self.word_guessed[i] = self.word[i]
            self.num_letters = self.num_letters - 1
        else:
            print("Sorry,", guess ,"is not in the word.")
            self.num_lives = self.num_lives - 1
            print("You have", self.num_lives,"lives left.")


    def ask_for_input(self):
        while True:
            guess = input("Enter your guess: ") 
            if len(guess) != 1 or guess.isalpha() == False:
                print('Invalid letter. Please, enter a single alphabetical character.')
            elif guess in self.list_of_guesses:
                print('You already tried that letter!')
            else:
                self.check_guess(guess)
                self.list_of_guesses.append(guess)
                print(self.word_guessed)
                break
                # if self.num_letters == 0:
                #     break

word_list_ = ['watermelon', 'apple', 'strawberries', 'blueberries', 'grapes']
my_hangman = Hangman(word_list_,5)
Hangman.ask_for_input(my_hangman)