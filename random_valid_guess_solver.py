
import random
from allowed_words_solver_helper import AllowedWordsSolverHelper
from constants import WORD_LENGTH
from wordleGame import WordleGame

class RandomValidGuessSolver:
    def __init__(self):
        self.reset()

    def guessNextWord(self):
        guess = random.choice(list(self.allowedWordsHelper.allowedWords))
        self.guesses.append(guess)
        return guess

    def reset(self):
        self.allowedWordsHelper = AllowedWordsSolverHelper()
        self.guesses = []
        game = WordleGame()

    def processGuessResult(self, guess, results, winningWord):
        self.allowedWordsHelper.processGuessResult(guess, results, winningWord)
