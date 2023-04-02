from typing import Dict
import random

class WordleWordDictionary:

    def __init__(self, wordlength):
        self.wordLength = wordlength
        self.loadWordFiles()

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

    def isValidGuess(self, word):
        if len(word) != self.wordLength:
            print("Invalid word length")
            return False
        if not self.isAllowedWord(word):
            print("Word is not allowed")
            return False
        return True

    def getNewWinningWord(self):
        winningWord = random.choice(list(self.winningWords))
        # print("winning word is " + winningWord)
        return winningWord
    
    def isValidGuess(self, word):
        if len(word) != self.wordLength:
            print("Invalid word length")
            return False
        if not self.isAllowedWord(word):
            print("Word is not allowed")
            return False
        return True
    
    def isAllowedWord(self, word):
        return word in self.allowedWords
