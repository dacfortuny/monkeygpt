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


def test_generate_answer_retries_on_invalid_response():
    insult = Insult("Test insult")
    responses = iter(
        [
            "Here's a great option!\n\nWhy this works: it's absurd and self-referential.",
            "So chickens as well?",
        ]
    )

    class FakeGenerator:
        def __init__(self, *args, **kwargs):
            pass

        def generate_text(self, prompt):
            return next(responses)

    with patch("src.answers.MistralTextGenerator", FakeGenerator):
        answer = AnswerPirate(insult, is_valid=True)

    assert answer.answer == "So chickens as well?"


def test_generate_answer_falls_back_after_repeated_invalid_responses():
    insult = Insult("Test insult")

    class FakeGenerator:
        def __init__(self, *args, **kwargs):
            pass

        def generate_text(self, prompt):
            return "Option 1: ...\nOption 2: ...\nWhy this works: ..."

    with patch("src.answers.MistralTextGenerator", FakeGenerator):
        answer = AnswerPirate(insult, is_valid=True)

    assert answer.answer == "I am rubber, you are glue"
