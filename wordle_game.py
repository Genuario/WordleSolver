from enum import Enum
import constants

from wordle_word_dictionary import WordleWordDictionary

class WordleGame:
    NOT_IN_WORD = 0
    IN_WORD = 1
    EXACT = 2

    def __init__(self, guessesPerGame = constants.NUM_GUESS_PER_GAME, wordLength = constants.WORD_LENGTH):
        self.guessesPerGame = guessesPerGame
        self.wordLength = wordLength
        self.loadWordleDictionary()
        self.resetGame()

    def loadWordleDictionary(self):
        self.wordDict = WordleWordDictionary(self.wordLength)

    # def readFile(self, fileName):
    #     fileObj = open(fileName, "r")
    #     words = fileObj.read().splitlines()
    #     fileObj.close()
    #     return words

    def resetGame(self, winningWord = None):
        self.guesses = []
        if winningWord is None:
            self.winningWord = self.wordDict.getNewWinningWord()
        else:
            self.winningWord = winningWord
        self.gameOver = False
        self.victory = False

    def startGame(self):
        # print("starting game")
        self.resetGame()
        
    def checkGameOver(self):
        if not self.gameOver:
            return False

        if self.victory:
            print("You already won")
        else:
            print("You already lost")
        return True


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
        if not self.wordDict.isValidGuess(word):
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
                if guessResults[i] == self.NOT_IN_WORD:
                    guessResults[i] = self.IN_WORD

        if len(self.guesses) == self.guessesPerGame:
            self.gameOver = True
        return guessResults

# class GuessResult(Enum):
#     NOT_IN_WORD = 0
#     IN_WORD = 1
#     EXACT = 2

