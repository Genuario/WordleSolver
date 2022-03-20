
class LlamaSolver:
    def __init__(self):
        self.reset()

    def guessNextWord(self):
        guess = "llama"
        self.guessResults.append(guess)
        return guess

    def reset(self):
        self.guessResults = []

    def processGuessResult(self, guessResult):
        x = guessResult

x = LlamaSolver()
