from avoid_loss_solver import AvoidLossSolver
from wordleGame import WordleGame

class InteractiveGame:
    def __init__(self):
        self.strat = AvoidLossSolver()
        self.validLetterResults = ['0', '1', '2']
        self.reset()

    def guessNextWord(self):
        guess = "llama"
        self.guessResults.append(guess)
        return guess

    def runGame(self):
        print("Starting game")
        self.reset()
        game = self.game
        game.startGame()
        firstParse = True
        while not self.gameOver:
            guess = self.getBestNextGuess()
            if guess is None:
                print("No possible guess. Did you enter a result incorrectly?")
                return
            self.parseNextGuess(guess, firstParse)
            firstParse = False

        
        self.checkIfPlayAgain()

    def parseNextGuess(self, guess, firstParse):
        if firstParse:
            print("""Enter the guess result for each letter
                0: Gray, not in word,
                1: Yellow, in word but wrong position
                2: Green, exact match
                Example: 10200
                """)
        else: 
            print("Enter the guess result")
        result = input()
        if not self.isValidUserResult(result):
            print("Invalid result <" + result + "> entered.")
            self.parseNextGuess(guess, True)
        if result == "22222":
            self.victory()
            return
        result = [int(x) for x in result]
        self.strat.processGuessResult(guess, list(result), None)

    def isValidUserResult(self, result):
        if not len(result) == 5:
            return False
        for letter in result:
            if not letter in self.validLetterResults:
                return False
        return True

    def getBestNextGuess(self):
        guess = self.strat.guessNextWord()
        print("You should guess: " + guess)
        return guess
    
    def victory(self):
        print("You won!")
        self.gameOver = True
    
    def checkIfPlayAgain(self):
        print("Play again? y/n")
        playAgain = input() == 'y'
        if playAgain:
            print("Starting new game")
            self.runGame()
        print("Exiting")

    def reset(self):
        self.game = WordleGame()
        self.strat.reset()
        self.gameOver = False

game = InteractiveGame()
game.runGame()