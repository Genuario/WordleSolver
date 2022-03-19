from enum import Enum
import random
from typing import Dict
import constants
class WordleGame:
    NOT_IN_WORD = 0
    IN_WORD = 1
    EXACT = 2

    def __init__(self, guessesPerGame = constants.NUM_GUESS_PER_GAME, wordLength = constants.WORD_LENGTH):
        self.guessesPerGame = guessesPerGame
        self.wordLength = wordLength
        self.loadWordFiles()
        self.resetGame()

    def loadWordFiles(self):
        self.allowedWords = set(self.readFile("wordle-allowed-guesses.txt"))
        self.winningWords = set(self.readFile("wordle-nyt-answers-alphabetical.txt"))
        # allowed words doesn't contain any winning words, so union the two
        self.allowedWords = self.allowedWords.union(self.winningWords)

    def readFile(self, fileName):
        fileObj = open(fileName, "r")
        words = fileObj.read().splitlines()
        fileObj.close()
        return words

    def resetGame(self, winningWord = None):
        self.guesses = []
        if winningWord is None:
            self.winningWord = self.getNewWinningWord()
        else:
            self.winningWord = winningWord
        self.gameOver = False
        self.victory = False

    def startGame(self):
        # print("starting game")
        self.resetGame()
    
    def getNewWinningWord(self):
        win = random.choice(list(self.winningWords))
        # print("winning word is " + win)
        return win

    def isValidGuess(self, word):
        if len(word) != self.wordLength:
            print("Invalid word length")
            return False
        if not self.isAllowedWord(word):
            print("Word is not allowed")
            return False
        return True
        
    def checkGameOver(self):
        if self.gameOver:
            if self.victory:
                print("You already won")
            else:
                print("You already lost")
            return True
        return False
    
    def isAllowedWord(self, word):
        return word in self.allowedWords


    '''
    Guess a word. 
    Returns
      'True' when game is won
      'False when guess is invalid
      'None' when game is over'
      'Array of int' when guess is valid but none-winning, where
         0: letter is not in word
         1: letter is in word, but in another position
         2: letter is correct
    '''
    def guessWord(self, word):
        # print("\nguessed word " + word)
        if self.checkGameOver():
            return None
        if not self.isValidGuess(word):
            return False
        if word == self.winningWord:
            self.victory = True
            self.gameOver = True
            return True
        self.guesses.append(word)
        guessResults = [self.NOT_IN_WORD] * 5
        winningWordCharMap = dict()
        for i, letter in enumerate(self.winningWord):
            if winningWordCharMap.get(letter) is None:
                winningWordCharMap[letter] = 0
            winningWordCharMap[letter] = winningWordCharMap[letter] + 1

        # First, check for exact letters,
        # removing them from the winningWordCharSet as we go.
        # We need to do this to ensure we don't get false
        # positive IN_WORD letters.
        # For example, if the wining word is 'xxxee'
        # and the user guesses 'eexee'
        # then the first 2 e's should return NOT_IN_WORD.
        for i, guessedLetter in enumerate(word):
            winningLetter = self.winningWord[i]
            if guessedLetter == winningLetter:
                guessResults[i] = self.EXACT
                winningWordCharMap[guessedLetter] = winningWordCharMap[guessedLetter] - 1
        
        # Next, check for IN_WORD letters
        for i, guessedLetter in enumerate(word):
            winningLetter = self.winningWord[i]
            if winningWordCharMap.get(guessedLetter) is not None and winningWordCharMap.get(guessedLetter) > 0:
                winningWordCharMap[guessedLetter] = winningWordCharMap[guessedLetter] - 1
                guessResults[i] = self.IN_WORD

        if len(self.guesses) == self.guessesPerGame:
            self.gameOver = True
        return guessResults

# class GuessResult(Enum):
#     NOT_IN_WORD = 0
#     IN_WORD = 1
#     EXACT = 2

