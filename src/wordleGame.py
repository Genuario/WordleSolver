from enum import Enum
import constants
class WordleGame
        self.guessesPerGame = guessesPerGame
        self.wordLength = wordLength
        self.loadWordFiles()
        self.resetGame()

    def loadWordFiles(self):
        self.allowedWords = set(self.readFile("..\wordle-allowed-guesses.txt"))
        self.winningWords = set(self.readFile("..\wordle-nyt-answers-alphabetical.txt"))
        # allowed words doesn't contain any winning words
        self.allowedWords = self.allowedWords.union(self.winningWords)
        print(self.winningWords)

    def readFile(self, fileName):
        fileObj = open(fileName, "r") #opens the file in read mode
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()
        return words

    def resetGame(self):
        self.guesses = []
        self.winningWord = "pizza"
        self.gameOver = False
        self.victory = False

    def startGame(self):
        print("starting game")
        self.resetGame()
        print(self.wordLength)
    
    def guessWord(self, word):
        print("guessed word " + word)
        if self.gameOver:
            if self.victory:
                print("You already won")
            else:
                print("You already lost")
            return False
        if len(word) != self.wordLength:
            print("Invalid word length")
            return False
        
        print(self.guesses)
        if word == self.winningWord:
            print("Victory!")
            self.victory = True
            self.gameOver = True
            return True
        self.guesses.append(word)
        guessResults = [GuessResult.NOT_IN_WORD * 5]
        
        winningWordCharSet = set(self.winningWord)

        # First, check for exact letters,
        # Removing them from the winningWordCharSet as we go
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
        print("exit guess")

class GuessResult(Enum):
    NOT_IN_WORD = 0
    IN_WORD = 1
    EXACT = 2
    

game = WordleGame(constants.NUM_GUESS_PER_GAME, constants.WORD_LENGTH)
game.startGame()
game.guessWord("these")
game.guessWord("blueberries")
game.guessWord("trees")
game.guessWord("please")
game.guessWord("alive")
game.guessWord("tones")
game.guessWord("friend")

game.guessWord("pizza")
