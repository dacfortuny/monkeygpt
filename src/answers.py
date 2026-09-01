from src.insult import Insult
from src.mistral_text_generator import MistralTextGenerator
from src.prompts import Prompt
from src.utils import get_insults


class Answer:
    def __init__(self, insult):
        self.insult = insult


class AnswerUser(Answer):
    def __init__(self, insult, text_input=None):
        super().__init__(insult)
        self.answer = text_input if text_input is not None else input("Write your answer.\n")


class AnswerPirate(Answer):
    FALLBACK_ANSWER = "I am rubber, you are glue"
    MAX_ANSWER_LENGTH = 500
    MAX_ATTEMPTS = 2

    def __init__(self, insult, is_valid):
        super().__init__(insult)
        self.answer = self._generate_answer(is_valid)
        self.is_fallback = self.answer == self.FALLBACK_ANSWER

    def _generate_answer(self, is_successful):
        if is_successful:
            insult = self.insult.insult
        else:
            insult = Insult().insult
        prompt = self._build_prompt(insult)
        text_generator = MistralTextGenerator()
        for _ in range(self.MAX_ATTEMPTS):
            answer = text_generator.generate_text(prompt.prompt)
            if self._is_valid_answer(answer):
                return answer.strip()
        return self.FALLBACK_ANSWER

    @staticmethod
    def _build_prompt(insult):
        prompt = Prompt()
        prompt.add_sentence(
            "\n\nHere you have examples of the insults used in the game and SUCCESSFUL answers:"
        )
        insults = get_insults().sample(frac=1).reset_index(drop=True).copy()
        insults["sentence"] = insults.apply(
            lambda row: f"\nInsult: {row['insult']}" f"\nSUCCESSFUL answer: {row['answer']}\n",
            axis=1,
        )
        prompt.add_sentence(f"\n{''.join(insults['sentence'])}")
        prompt.add_sentence("\nGenerate a SUCCESSFUL for the following insult:\n")
        prompt.add_sentence(f"\nInsult: {insult}\nSUCCESSFUL answer: ")
        return prompt

    @classmethod
    def _is_valid_answer(cls, answer):
        # The model occasionally returns multi-option, explanatory rambling
        # instead of a single in-character quip, e.g. "Why this works: ...".
        if not answer:
            return False
        cleaned = answer.strip()
        return bool(cleaned) and "\n" not in cleaned and len(cleaned) <= cls.MAX_ANSWER_LENGTH
