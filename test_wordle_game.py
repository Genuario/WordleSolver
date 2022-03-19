# import pytest
from wordleGame import WordleGame

class TestWordleGame:
    def test_can_create_wordle_game(self):
        game = WordleGame()
        assert game is not None

    def test_when_seven_letter_word_get_false(self):
        game = WordleGame()
        response = game.guessWord("unicorn")
        assert response is False

    def test_when_one_letter_word_get_false(self):
        game = WordleGame()
        response = game.guessWord("a")
        assert response is False

    def test_when_guess_fake_word_get_false(self):
        game = WordleGame()
        response = game.guessWord("xxxxx")
        assert response is False

    def test_when_guess_valid_word_get_not_false(self):
        game = WordleGame()
        response = game.guessWord("soare")
        assert response is not False

    def test_when_guess_invalid_word_six_times_game_not_over(self):
        game = WordleGame()
        for x in range(6):
            game.guessWord("xxxxx")
        response = game.guessWord("soare")
        assert response is not None
        assert game.gameOver is False

    def test_when_guess_valid_word_six_times_game_is_over(self):
        game = WordleGame()
        for x in range(6):
            game.guessWord("soare")
        response = game.guessWord("soare")
        assert response is None
        assert game.gameOver is True

    def test_when_guess_winning_word_game_over(self):
        game = WordleGame()
        game.resetGame("soare")
        response = game.guessWord("soare")
        assert response is True
        assert game.gameOver is True


    def test_when_guess_winning_word_after_game_over_still_game_over(self):
        game = WordleGame()
        game.resetGame("soare")
        for x in range(6):
            game.guessWord("lucky")
        response = game.guessWord("soare")
        assert response is None
        assert game.gameOver is True

    def test_when_guess_winning_word_on_sixth_guess_win(self):
        game = WordleGame()
        game.resetGame("soare")
        for x in range(5):
            game.guessWord("lucky")
        response = game.guessWord("soare")
        assert response is True
        assert game.gameOver is True

    def test_when_guess_matching_letter_get_hints(self):
        game = WordleGame()
        game.resetGame("table")
        response = game.guessWord("fable")
        assert response is not None
        guessResults = [WordleGame.EXACT] * 5
        guessResults[0] = WordleGame.NOT_IN_WORD
        assert response == guessResults

    def test_when_guess_no_matching_letter_get_all_not_in_words(self):
        game = WordleGame()
        game.resetGame("table")
        response = game.guessWord("muddy")
        assert response is not None
        guessResults = [WordleGame.NOT_IN_WORD] * 5
        assert response == guessResults

    def test_when_guess_wrong_positionmatching_letter_get_hints(self):
        game = WordleGame()
        game.resetGame("table")
        response = game.guessWord("chair")
        assert response is not None
        guessResults = [WordleGame.NOT_IN_WORD] * 5
        guessResults[2] = WordleGame.IN_WORD
        assert response == guessResults

    def test_when_guess_duplicate_letters_only_first_in_word(self):
        game = WordleGame()
        game.resetGame("soare")
        response = game.guessWord("dross")
        assert response is not None
        guessResults = [WordleGame.NOT_IN_WORD,
                        WordleGame.IN_WORD,
                        WordleGame.IN_WORD,
                        WordleGame.IN_WORD,
                        WordleGame.NOT_IN_WORD ]
        assert response == guessResults

    def test_when_duplicate_letters_in_winning_word_multiple_guesssed_letters_count(self):
        game = WordleGame()
        game.resetGame("agree")
        response = game.guessWord("deets")
        assert response is not None
        guessResults = [WordleGame.NOT_IN_WORD,
                        WordleGame.IN_WORD,
                        WordleGame.IN_WORD,
                        WordleGame.NOT_IN_WORD,
                        WordleGame.NOT_IN_WORD ]
        assert response == guessResults
