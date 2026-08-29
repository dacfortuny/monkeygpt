from unittest.mock import patch

from src.assault import Assault


class FakeInsult:
    def __init__(self, text):
        self.insult = text


class FakeAnswer:
    def __init__(self, text):
        self.answer = text


class FakeGenerator:
    def __init__(self, response):
        self.response = response

    def __call__(self, *args, **kwargs):
        return self

    def generate_text(self, prompt):
        return self.response


def _evaluate(response_text):
    assault = Assault(FakeInsult("Ye be a scurvy dog"), FakeAnswer("Aye, and proud of it"))
    with patch("src.assault.MistralTextGenerator", FakeGenerator(response_text)):
        return assault.evaluate_insult_success()


def test_evaluate_insult_success_true_on_yes():
    assert _evaluate("Yes") is True


def test_evaluate_insult_success_true_on_yes_with_trailing_text():
    assert _evaluate("Yes, definitely successful.") is True


def test_evaluate_insult_success_false_on_no():
    assert _evaluate("No") is False


def test_evaluate_insult_success_false_on_unrecognized_response():
    assert _evaluate("unclear") is False
