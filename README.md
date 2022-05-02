# WordleSolver
Always win in Wordle! Simulates and optimizes to never lose. Uses the NYTimes winning words and allowed guesses txt files.


## How to play
Open your favorite Wordle web browser. The game will provide the best word for you to guess. After each guess, you'll enter the result for each letter.

`python .\play_game.py`

## How to run simulations

Simulate running all words. The StrategyRunner will take in a stragegy, which simply exposes a `guessNextWord` function. Using that strategy, it will simulate a Wordle Game for each winning word and log the results.

`python .\run_strategies.py`

## Avoid_loss_solver
This solver can consistently solve every winning word in wordle. 
Answers are deterministic. Results never vary.
```
Simulation results:
wins: 2309 losses: 0
```

This solver optimizes to never lose. Consequently, for easier words, it may make suboptimal guesses to ensure it never loses to harder words. A different solver could optimize to minimize the average number of guesses, but accept failure for the most difficult words.

### Guess Distribution

| Num Guesses | Num Words   |
|---|-----|
| 1 | 1   |
| 2 | 73  |
| 3 | 530 |
| 4 | 960 |
| 5 | 646 |
| 6 | 90  |

### Commits
Use https://gitmoji.dev/
