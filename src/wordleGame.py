from enum import Enum
import random
import constants
class WordleGame:
    def __init__(self, guessesPerGame, wordLength):
        self.guessesPerGame = guessesPerGame
        self.wordLength = wordLength
        self.loadWordFiles()
        self.resetGame()

    def loadWordFiles(self):
        self.allowedWords = set(self.readFile("..\wordle-allowed-guesses.txt"))
        self.winningWords = set(self.readFile("..\wordle-nyt-answers-alphabetical.txt"))
        # allowed words doesn't contain any winning words, so union the two
        self.allowedWords = self.allowedWords.union(self.winningWords)

    def readFile(self, fileName):
        fileObj = open(fileName, "r")
        words = fileObj.read().splitlines()
        fileObj.close()
        return words

    def resetGame(self):
        self.guesses = []
        self.winningWord = self.getNewWinningWord()
        self.gameOver = False
        self.victory = False

    def startGame(self):
        print("starting game")
        self.resetGame()
        print(self.wordLength)
    
    def getNewWinningWord(self):
        win = random.choice(list(self.winningWords))
        print("winning word is " + win)
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

    def guessWord(self, word):
        print("\nguessed word " + word)
        print(self.guesses)
        if self.checkGameOver() or not self.isValidGuess(word):
            print("exit1")
            return False
        if word == self.winningWord:
            print("Victory!")
            self.victory = True
            self.gameOver = True
            return True
        print("hello")
        self.guesses.append(word)
        guessResults = [GuessResult.NOT_IN_WORD] * 5
        winningWordCharSet = set(self.winningWord)

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
                guessResults.insert(i, GuessResult.EXACT)
                winningWordCharSet.remove(guessedLetter)
        
        # Next, check for IN_WORD letters
        for i, guessedLetter in enumerate(word):
            winningLetter = self.winningWord[i]
            if guessedLetter in winningWordCharSet:
                winningWordCharSet.remove(guessedLetter)
                guessResults.insert(i, GuessResult.IN_WORD)

        if len(self.guesses) == self.guessesPerGame:
            self.gameOver = True
        print(guessResults)

class GuessResult(Enum):
    NOT_IN_WORD = 0
    IN_WORD = 1
    EXACT = 2
    

game = WordleGame(constants.NUM_GUESS_PER_GAME, constants.WORD_LENGTH)
game.startGame()
game.guessWord("these")
game.guessWord("xxxxx")
game.guessWord("blueberries")
game.guessWord("nicer")
game.guessWord("tiger")
game.guessWord("alive")
game.guessWord("tones")
game.guessWord("pines")
game.guessWord("pizza")
