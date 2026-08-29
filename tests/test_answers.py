from unittest.mock import patch

from src.answers import AnswerPirate
from src.insult import Insult


def test_generate_answer_builds_per_row_examples():
    insult = Insult("Test insult")
    captured = {}

    class FakeGenerator:
        def __init__(self, *args, **kwargs):
            pass

        def generate_text(self, prompt):
            captured["prompt"] = prompt
            return "A witty comeback"

    with patch("src.answers.MistralTextGenerator", FakeGenerator):
        answer = AnswerPirate(insult, is_valid=True)

    assert answer.answer == "A witty comeback"
    prompt = captured["prompt"]
    assert "Insult:" in prompt
    assert "SUCCESSFUL answer:" in prompt
    # Regression: building the example block used to f-string the whole
    # pandas Series in one go, leaking its repr into the prompt instead of
    # one line per example.
    assert "dtype: object" not in prompt
    assert "Name: insult" not in prompt
