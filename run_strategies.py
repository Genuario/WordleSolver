from random_valid_guess_solver import RandomValidGuessSolver
from constants import NUM_GUESS_PER_GAME
from avoid_loss_solver import AvoidLossSolver
from wordleGame import WordleGame

class StrategyRunner:
    def __init__(self):
        game = WordleGame()
        self.winningWords = game.winningWords

    def guessWord(self, game, strat, winningWord):
        guess = strat.guessNextWord()
        result = game.guessWord(guess)
        if result == True:
            return True
        strat.processGuessResult(guess, result, winningWord)

    def runGame(self, game, strat, winningWord):
       # print("WINNING WORD IS " + winningWord)
        for x in range(NUM_GUESS_PER_GAME):
            gameOver = self.guessWord(game, strat, winningWord)
            if gameOver:
                return True
        
    
    def runStrategyForAllWinningWords(self, strat, saveLosingWords):
        numWinningWords = len(self.winningWords)
        losingWords = []
        print("Starting simulation for all " + str(numWinningWords) + " winning words ")
        winCount = 0
        lossCount = 0
        soFar = 0
        game = WordleGame()
        for word in self.winningWords:
            game.resetGame(word)
            # game.resetGame()
            strat.reset()
            self.runGame(game, strat, game.winningWord)


            if game.victory:
                winCount = winCount + 1
            else:
                lossCount = lossCount + 1
                if saveLosingWords:
                    losingWords.append(word)
            
            soFar = soFar + 1
            if (soFar % 100) == 0:
                print("processed " + str(soFar) + "/" + str(numWinningWords))
        losingWords.sort()
        print(losingWords)
        print("Simulation results:\nwins: " + str(winCount) + " losses: " +  str(lossCount))

        return winCount, lossCount

# s = StrategyRunner()
# strat = LlamaSolver()
# s.runStrategyForAllWinningWords(strat)

s = StrategyRunner()
strat = AvoidLossSolver()
s.runStrategyForAllWinningWords(strat, True)
game = WordleGame()
vic = True
# while vic:
#     game.resetGame("catch")
#     strat.reset()
#     s.runGame(game, strat, game.winningWord)
#     vic = game.victory
#     print(game.victory)
#     # break
# ['bound', 'brave', 'break', 'catch', 'cider', 'class', 'cover', 'craft', 'crave', 'dandy', 'diner', 'dough', 'dowel', 'exile', 'fight', 'flack', 'foist', 'folly', 'foyer', 'gauge', 'grace', 'grade', 'greed', 'grown', 'gully', 'hatch', 'hilly', 'joker', 'mince', 'miner', 'mound', 'parer', 'rider', 'rover', 'rower', 'scare', 'shake', 'silly', 'slash', 'stout', 'sully', 'swash', 'tasty', 'tatty', 'tight', 'whose']

# ['foyer', 'gauge', 'glaze', 'homer', 'nanny', 'slash', 'wider']
#['gauge', 'mealy', 'rider']

# ['craze', 'crook', 'drool', 'maize', 'vague']
# ['craze', 'crock', 'drool', 'gauze', 'maize']
# ['crock', 'drool', 'maize', 'vague']
# ['crock', 'drool', 'vague', 'waive']

# ['craze', 'crock', 'crook', 'drool', 'gauze', 'maize', 'vague', 'waive']

# ['brace', 'chose', 'crane', 'crock', 'drool', 'gauze', 'leafy', 'maize', 'match', 'rider', 'watch']

# ['gauze', 'waive']

# ['blame', 'drier', 'leave', 'stake', 'state', 'tease']

# ['skate', 'state', 'tease']