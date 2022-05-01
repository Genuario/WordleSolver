
import random
from unittest import TextTestRunner
from allowed_words_solver_helper import AllowedWordsSolverHelper
from constants import WORD_LENGTH
from wordleGame import WordleGame

class AvoidLossSolver:
    def __init__(self):
        self.reset()
        self.bestFirstGuess = self.getHighestScoringWord(self.allowedWordsHelper.allowedWords, False)
        self.bestSecondGuess = "fungi"

    def guessNextWord(self):
        doPrint = False # Set this to True to get 
        guess = None
        # Because the best first guess will be the same for every game, 
        # we can determine the value once and set it for all games.
        if len(self.guesses) == 0:
            guess = self.bestFirstGuess
        # If we get little information from the first guess, then use the default
        # second guess
        # TODO: Dynamically calculate this value instead of using hardcoded
        elif len(self.guesses) == 1 and self.shouldUseDefaultBestSecondGuess():
            guess = self.bestSecondGuess
        else: 
            guess = self.getHighestScoringWord(self.allowedWordsHelper.allowedWords, doPrint)
        
        if doPrint:
            lettersLeft = len(self.getUnkownLettersRemaining())
            wordsLeft = len(self.allowedWordsHelper.allowedWords)
            guessesLeft = self.getNumGuessesRemaining()
            print("\n***guessing " + guess)
            print("with knowledge wordsLeft " + str(wordsLeft) + " lettersLeft = " + str(lettersLeft) + " guessesLeft = " + str(guessesLeft))
            print("requiredLetters = ") 
            print(self.allowedWordsHelper.requiredLetters)
            print("exactLetters")
            print(self.allowedWordsHelper.exactLetters)
            if lettersLeft <= 12:
                print("unknown letters")
                unknown = list(self.getUnkownLettersRemaining())
                unknown.sort()
                print(unknown)
            if wordsLeft < 10:
                print(self.allowedWordsHelper.allowedWords)
                print(freqMap)

        self.guesses.append(guess)
        return guess
    
    def shouldUseDefaultBestSecondGuess(self):
        return len(self.allowedWordsHelper.requiredLetters) < 2 or (len(self.allowedWordsHelper.requiredLetters) == 2 and self.areAllVowels(self.allowedWordsHelper.requiredLetters))  
    
    def areAllVowels(self, letters):
        for letter in letters:
            if not letter in self.allowedWordsHelper.vowels:
                return False
        return True
    
    def getNumGuessesRemaining(self):
        return 6 - len(self.guesses)
    
    def getUnkownLettersRemaining(self):
        return self.allowedWordsHelper.unknownLettersRemaining

    def getUnkownLettersRemainingWordMap(self):
        return self.allowedWordsHelper.unknownLettersRemainingWordMap

    def containsDupLetter(self, word):
        seenLetters = set()
        for letter in word:
            if letter in seenLetters:
                return False
            seenLetters.add(letter)
        return True

    def getWordScoreByCharFreq(self, word, freqMap):
        score = 0
        dupLetterPenalty = 1
        seenLetters = []
        for i, letter in enumerate(word):
            letterScore = 0
            
            if letter not in seenLetters:
                for j in range(5):
                    if i != j:
                        letterJScore = freqMap[j].get(letter)
                        letterJScore = letterJScore if letterJScore else 0
                        letterScore += letterJScore
            else:
                dupLetterPenalty /= 10
            seenLetters.append(letter)
            score += letterScore if letterScore else 0
        score *= dupLetterPenalty

        score = score / 10
        return score
    
    # When there are few letters remaining with many shared letters, we should
    # prioritize eliminating multiple letters with one guess
    # Example when ['hound', 'wound', 'mound', 'bound', 'found']
    #         then prioritize 'hwmbd' instead of 'ound'
    def getWordScoreByLettersRemaining(self, word, lettersLeft):
        score = 0
        unseenLetters = []
        for letter in lettersLeft:
            unseenLetters.append(letter)
        for letter in self.allowedWordsHelper.requiredLetters:
            if letter in unseenLetters:
                unseenLetters.append(letter)
        
        for letter in word:
            if letter in lettersLeft and letter in unseenLetters:
                unseenLetters.remove(letter)
                if letter not in unseenLetters:
                    score += 1
        return score

    def getWordScoreByLettersRemainingWithWordTracking(self, word, lettersLeft):
        letterToWordsMap = self.allowedWordsHelper.unknownLettersRemainingWordMap
        # Map contains potential unknown letters, mapped to the word they're from.
        # Once a word is removed from any letter, we should ignore it in the other words as well to ensure
        # we don't give points to 2 letters from the same word.
        # For ex: ['growl', 'drool', 'droll']
        # Picking both G and W would should only give us 1 point of info, since they're only contained with 'growl'
        score = 0
        unseenLetters = []
        for letter in lettersLeft:
            unseenLetters.append(letter)
        for letter in self.allowedWordsHelper.requiredLetters:
            if letter in unseenLetters:
                unseenLetters.append(letter)
        
        for letter in word:
            if letter in lettersLeft and letter in unseenLetters:
                unseenLetters.remove(letter)
                if letter not in unseenLetters:
                    wordsWithLetter = letterToWordsMap.get(letter)
                    if wordsWithLetter != None and len(wordsWithLetter) != 0:
                        # remove all these words from the rest of the map
                        self.removeWordsFromWordMap(letterToWordsMap, wordsWithLetter)
                        score += 1
        return score

    # could map 2 dir map, but this is simpler for now
    def removeWordsFromWordMap(self, letterToWordsMap, wordsWithLetter):
        letterToWordsMapCopy = dict()
        for letter in letterToWordsMap:
            if letterToWordsMap.get(letter) != None:
                letterToWordsMapCopy[letter] = letterToWordsMap[letter].copy()
        for word in wordsWithLetter:
            for letterKey in letterToWordsMap:
                if word in letterToWordsMapCopy[letterKey]:
                    letterToWordsMapCopy[letterKey].remove(word)
        
        letterToWordsMap = letterToWordsMapCopy
    def getHighestScoringWordTripleStrat(self, allowedWords, doPrint):
        # Check if 1 letter is shared among exactly 2 of the words.
        # If so, we can guess one of those 2 words. Doing so will either
        #   1. Win 
        #   2. Leave only the 3rd word remaining (with no shared letter)
        #   3. Give a match for the letter but not the word,
        #      which means it's the 2nd word
        for word in allowedWords:
            for i in range(WORD_LENGTH):
                letterMatches = 0
                for otherWord in allowedWords:
                    if word != otherWord and word[i] == otherWord[i]:
                        letterMatches = letterMatches + 1
                if letterMatches == 1:
                    return word
        
        # If we've gotten to this point, then we didn't find an optimal word.
        # resort to default strat
        return None

    def isChich(self, allowedWords):
        return "hatch" in allowedWords and "catch" in allowedWords

    ## Simply add each char freq together
    def getHighestScoringWord(self, allowedWords, doPrint):
        freqMap = self.getCharFrequency(self.allowedWordsHelper.allowedWords)
        highestScoreWord = None
        highestScore = -1
        numRemainingWords = len(allowedWords)
        lettersLeft = self.getUnkownLettersRemaining()
        numLettersLeft = len(lettersLeft)
        guessesLeft = self.getNumGuessesRemaining()

        if numRemainingWords == 1:
            if doPrint:
                print("only 1 word left")
            return allowedWords.pop()
        elif numRemainingWords == 3 and guessesLeft == 2:
            if doPrint:
                print("TRIPLE STRAT")
            # if there's 3 words left and 2 guesses,see if we can kill 2 birds with one stone
            highestScoreWord = self.getHighestScoringWordTripleStrat(allowedWords, doPrint)
            if highestScoreWord == None:
                highestScoreWord = self.getHighestScoringWordEliminationStrat(lettersLeft, freqMap, doPrint)
            # simulate remaining words by 
        # elif numRemainingWords < 10 and guessesLeft >= 3 and self.isChich(allowedWords):
        #     return "chich"
        elif numRemainingWords > guessesLeft and ((numLettersLeft <= 11 and guessesLeft > 1) or (guessesLeft == 3 and numLettersLeft < 8) or (guessesLeft == 4 and numLettersLeft == 16)):
            if doPrint:
                print("ELIMINATION STRAT")
            highestScoreWord = self.getHighestScoringWordEliminationStrat(lettersLeft, freqMap, doPrint)
        else:
            if doPrint:
                print("FREQ STRAT")
            for word in allowedWords:
                if numRemainingWords == 3:
                    if doPrint:
                        print("testing guess word " + word)
                score = self.getWordScoreByCharFreq(word, freqMap)

                if score > highestScore:
                    highestScore = score
                    highestScoreWord = word

        return highestScoreWord
        
    def reset(self):
        self.allowedWordsHelper = AllowedWordsSolverHelper()
        self.guesses = []
        game = WordleGame()

    def processGuessResult(self, guess, results, winningWord):
        self.allowedWordsHelper.processGuessResult(guess, results, winningWord)
    
    def getCharFrequency(self, words):
        freqMap = dict()
        for i in range(WORD_LENGTH):
            freqMap[i] = dict()
        
        for word in words:
            for i, letter in enumerate(word):
                if freqMap[i].get(letter) is None:
                    freqMap[i][letter] = 0
                freqMap[i][letter] = freqMap[i][letter] + 1
        return freqMap


    def getHighestScoringWordEliminationStrat(self, lettersLeft, freqMap, doPrint):
        highestScoreWord = None
        highestScore = -1
        for word in self.allowedWordsHelper.allowedGuesses:
            score = -1
            if len(self.allowedWordsHelper.allowedWords) <=0 :
                score = self.getWordScoreByLettersRemainingWithWordTracking(word, lettersLeft)
            else:
                score = self.getWordScoreByLettersRemaining(word, lettersLeft)
            if score == highestScore:
                prevHighScoreFreq = self.getWordScoreByCharFreq(word, freqMap)
                curHighScoreFreq = self.getWordScoreByCharFreq(highestScoreWord, freqMap)
                if prevHighScoreFreq == curHighScoreFreq:
                    curWordWinningWord = highestScoreWord in self.allowedWordsHelper.winningWords
                    newWordWinningWord = word in self.allowedWordsHelper.winningWords
                    if newWordWinningWord and not curWordWinningWord:
                        if doPrint:
                            print("***replace " + highestScoreWord + str(curHighScoreFreq) + " with " + word + str(prevHighScoreFreq) )
                        highestScore = score
                        highestScoreWord = word
                elif prevHighScoreFreq > curHighScoreFreq:
                    if doPrint:
                        print(" replace " + highestScoreWord + str(curHighScoreFreq) + " with " + word + str(prevHighScoreFreq) )
                    highestScore = score
                    highestScoreWord = word
            elif score > highestScore:
                highestScore = score
                highestScoreWord = word
        if highestScoreWord == None:
            print("we should never reach this")
        return highestScoreWord