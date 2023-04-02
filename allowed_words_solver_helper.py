
from pickle import NONE
import random
from re import L
from constants import WORD_LENGTH
from wordle_game import WordleGame
import string


class AllowedWordsSolverHelper:
    def __init__(self):
        self.reset()

    def reset(self):
        self.guessResults = []
        self.guesses = []
        game = WordleGame()
        self.allowedGuesses = game.wordDict.allowedWords
        self.allowedWords = game.wordDict.winningWords
        self.winningWords = game.wordDict.winningWords
        self.exactLetters = [None] * 5
        self.initPossibleLetters()
        self.requiredLetters = []
        self.updateUnknownLettersRemaining()
        self.updateUnknownLettersRemainingWordMap()
        self.vowels = ['a', 'e', 'i', 'o', 'u']

    def initPossibleLetters(self):
        self.possibleLetters = []
        for i in range(WORD_LENGTH):
            self.possibleLetters.append(set())
            for l in list(string.ascii_lowercase):
                self.possibleLetters[i].add(l)

    def isUnknownLetter(self, letter):
        return letter not in self.requiredLetters
    
    def isLetterInGuess(self, guess, letter):
        for l in guess:
            if letter == l:
                return True
        return False

    def getFreqCounts(self, letterArray):
        counts = dict()
        for letter in letterArray:
            if letter not in counts:
                counts[letter] = 0
            counts[letter] = counts[letter] + 1
        return counts


    # Given two dicts, merge them together, then return in array form    
    def mergeFreqCounts(self, dictOld, dictNew):
        counts = dictOld
        for key in dictNew:
            oldCount = 0
            if key in counts:
                oldCount = counts[key]
            counts[key] = max(oldCount, dictNew[key])

        flattenArray = []
        for key in counts:
            count = counts[key]
            for i in range(count):
                flattenArray.append(key)
        return flattenArray
    
    def updateRequiredLetters(self, newRequiredLetters):
        dictOld = self.getFreqCounts(newRequiredLetters)
        dictNew = self.getFreqCounts(self.requiredLetters)
        self.requiredLetters = self.mergeFreqCounts(dictOld, dictNew)

    def processGuessResult(self, guess, results, winningWord):
        self.guessResults.append(results)
        newRequiredLetters = []
        for i, result in enumerate(results):
            letter = guess[i]
            if result == WordleGame.EXACT:
                self.exactLetters[i] = letter
                newRequiredLetters.append(letter)
            elif result == WordleGame.IN_WORD:
                if letter in self.possibleLetters[i]:
                    self.possibleLetters[i].remove(letter)
                # if not letter in self.requiredLetters:
                newRequiredLetters.append(letter)
            elif result == WordleGame.NOT_IN_WORD:
                if letter in self.requiredLetters or letter in newRequiredLetters:
                    if letter in self.possibleLetters[i]:
                        self.possibleLetters[i].remove(letter)
                else:
                    # Remove the letter as a possibility
                    for j in range(WORD_LENGTH):
                        if letter in self.possibleLetters[j]:
                            self.possibleLetters[j].remove(letter)
            else:
                print("Invalid result entered!" + result)
        self.updateRequiredLetters(newRequiredLetters)

        if guess in self.allowedWords:
            self.allowedWords.remove(guess)
        self.updateRemainingWords(winningWord)

        # Check if we know a letter because all remaining words share that letter
        self.checkIfKnowMoreLetters()
        self.updateUnknownLettersRemaining()

    def checkIfOnlyOneLetter(self, letterIndex):
        if self.exactLetters[letterIndex] != None:
            return None
        sharedLetter = None
        for word in self.allowedWords:
            newLetter = word[letterIndex]
            if sharedLetter == None:
                sharedLetter = newLetter
            else:
                if newLetter != sharedLetter:
                    return None
        return sharedLetter

    def checkIfKnowMoreLetters(self):
        for letterIndex in range(WORD_LENGTH):
            sharedLetter = self.checkIfOnlyOneLetter(letterIndex)
            if sharedLetter != None:
                self.exactLetters[letterIndex] = sharedLetter
                if sharedLetter not in self.requiredLetters:
                    self.requiredLetters.append(sharedLetter)

    def updateRemainingWords(self, winningWord):
        newAllowedWords = []
        # Remove non exact characters
        for word in self.allowedWords:
            resp = self.isAllowedWord(word, winningWord)
            if resp is True:
                newAllowedWords.append(word)
        self.allowedWords = newAllowedWords

    def getNumMatchedLetters(self):
        count = 0
        for l in self.requiredLetters:
            if l != None:
                count = count + 1
        return count

    def isAllowedWord(self, word, winningWord):
        doLog = word == winningWord
        countBefore = len(self.requiredLetters)
        unseenRequiredLetters = self.requiredLetters.copy()
        for i, letter in enumerate(word):
            if self.exactLetters[i] is not None:
                if letter != self.exactLetters[i]:
                    if doLog:
                        print("BAD exact letter bad " + str(i) + " " + letter)
                    return False
            elif not letter in self.possibleLetters[i]:
                if doLog and winningWord:
                    print("BAD possible letter bad " + str(i) + " " + letter + " desired=" + winningWord[i])
                return False
            if letter in unseenRequiredLetters:
                unseenRequiredLetters.remove(letter)
                # if doLog:
                #     print("remove letter good " + str(i) + " " + letter)
                # seenRequiredLetters.add(letter)

        # print("bagel " + str(countBefore))
        if countBefore != len(self.requiredLetters):
            print("VERY BAD")
        if doLog:
            r = len(unseenRequiredLetters) != 0
            if r:
                print("removing")
                print(unseenRequiredLetters)
        return len(unseenRequiredLetters) == 0
        # return len(seenRequiredLetters) == len(self.requiredLetters)

    def updateUnknownLettersRemaining(self):
        unknownLettersLeft = set()

        # getFreqCounts
        for word in self.allowedWords:
            unseenRequiredLetters = self.requiredLetters.copy()
            for letter in word:
                if letter not in unseenRequiredLetters: # unknown letter
                    unknownLettersLeft.add(letter)
                else:
                    unseenRequiredLetters.remove(letter)
        
        self.unknownLettersRemaining = unknownLettersLeft
    
    # Maps remaining unknown letters to the word they're from
    def updateUnknownLettersRemainingWordMap(self):
        unknownLettersWordMap = dict()

        if len(self.allowedWords) >= 0:
            self.unknownLettersRemainingWordMap = unknownLettersWordMap
            return

        # getFreqCounts
        for word in self.allowedWords:
            unseenRequiredLetters = self.requiredLetters.copy()
            for letter in word:
                if letter not in unseenRequiredLetters: # unknown letter
                    if unknownLettersWordMap.get(letter) == None:
                         unknownLettersWordMap[letter] = set()
                    unknownLettersWordMap[letter].add(word)
                else:
                    unseenRequiredLetters.remove(letter)
        
        self.unknownLettersRemainingWordMap = unknownLettersWordMap