from constants import NUM_GUESS_PER_GAME
from llama_solver import LlamaSolver
from wordleGame import WordleGame

class StrategyRunner:
    def __init__(self):
        game = WordleGame()
        self.winningWords = game.winningWords

    def runStrategyForAllWinningWords(self, strat):
        numWinningWords = len(self.winningWords)
        print("Starting simulation for all " + str(numWinningWords) + " winning words ")
        winCount = 0
        lossCount = 0
        soFar = 0
        for word in self.winningWords:
            game = WordleGame()
            game.resetGame(word)
            strat.reset()

            for x in range(NUM_GUESS_PER_GAME):
                guess = strat.guessNextWord()
                result = game.guessWord(guess)
                strat.processGuessResult(result)
            if game.victory:
                winCount = winCount + 1
            else:
                lossCount = lossCount + 1
            
            soFar = soFar + 1
            if (soFar % 100) == 0:
                print("processed " + str(soFar) + "/" + str(numWinningWords))
        
        print("Simulation results:\nwins: " + str(winCount) + " losses: " +  str(lossCount))
        return winCount, lossCount

strat = LlamaSolver()
s = StrategyRunner()
s.runStrategyForAllWinningWords(strat)