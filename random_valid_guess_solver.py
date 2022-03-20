
from operator import contains
import random
import winsound
from constants import WORD_LENGTH
from wordleGame import WordleGame
import string


class RandomValidGuessSolver:
    def __init__(self):
        self.reset()

    def guessNextWord(self):
        ## self.getCharFrequency(self.allowedWords)
        guess = random.choice(list(self.allowedWords))

        self.guesses.append(guess)
        return guess

    def reset(self):
        self.guessResults = []
        self.guesses = []
        game = WordleGame()
        self.allowedWords = game.winningWords # todo make allowed
        self.exactLetters = [None] * 5
        self.initPossibleLetters()
        self.requiredLetters = set()

    def initPossibleLetters(self):
        self.possibleLetters = []
        for i in range(WORD_LENGTH):
            self.possibleLetters.append(set())
            for l in list(string.ascii_lowercase):
                self.possibleLetters[i].add(l)

    def isLetterInGuess(self, guess, letter):
        for l in guess:
            if letter == l:
                return True
        return False
    
    def processGuessResult(self, guess, results, winningWord):
        self.guessResults.append(results)
        for i, result in enumerate(results):
            letter = guess[i]
            if result == WordleGame.EXACT:
                self.exactLetters[i] = letter
            elif result == WordleGame.IN_WORD:
                if letter in self.possibleLetters[i]:
                    self.possibleLetters[i].remove(letter)
                if not letter in self.requiredLetters:
                    self.requiredLetters.add(letter)
            elif result == WordleGame.NOT_IN_WORD:
                for j in range(WORD_LENGTH):
                    if not self.isLetterInGuess(guess, letter):
                        if letter in self.possibleLetters[j]:
                            self.possibleLetters[j].remove(letter)
        
        self.allowedWords.remove(guess)
        self.updateRemainingWords(winningWord)
        c = winningWord in self.allowedWords
        if c is False:
            print("BAD STATE " + winningWord)

    def updateRemainingWords(self, winningWord):
        newAllowedWords = []
        # Remove non exact characters
        for word in self.allowedWords:
            resp = self.isAllowedWord(word, winningWord)
            if resp is True:
                newAllowedWords.append(word)
        # print("allowed words before " + str(len(self.allowedWords)) + " after " + str(len(newAllowedWords)))
        self.allowedWords = newAllowedWords

            
    def isAllowedWord(self, word, winningWord):
        seenRequiredLetters = set()
        for i, letter in enumerate(word):
            if self.exactLetters[i] is not None:
                if letter != self.exactLetters[i]:
                    return False
            elif not letter in self.possibleLetters[i]:
                return False
            if letter in self.requiredLetters:
                seenRequiredLetters.add(letter)

        return len(seenRequiredLetters) == len(self.requiredLetters)

    def getCharFrequency(self, words):
        freqMap = dict()
        for i in range(WORD_LENGTH):
            freqMap[i] = dict()
        
        for word in words:
            for i, letter in word:
                if freqMap[i].get(letter) is None:
                    freqMap[i][letter] = 0
                freqMap[i][letter] = freqMap[i][letter] + 1
        return freqMap