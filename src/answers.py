from src.insult import Insult
from src.mistral_text_generator import MistralTextGenerator
from src.prompts import Prompt
from src.utils import get_insults


class Answer:
    def __init__(self, insult):
        self.insult = insult


class AnswerUser(Answer):
    def __init__(self, insult):
        super().__init__(insult)
        self.answer = input("Write your answer.\n")


class AnswerPirate(Answer):
    def __init__(self, insult, is_valid):
        super().__init__(insult)
        self.answer = self._generate_answer(is_valid)

    def _generate_answer(self, is_successful):
        if is_successful:
            insult = self.insult.insult
        else:
            insult = Insult().insult
        text_generator = MistralTextGenerator()
        prompt = Prompt()
        prompt.add_sentence(
            "\n\nHere you have examples of the insults used in the game and SUCCESSFUL answers:"
        )
        insults = get_insults().sample(frac=1).reset_index(drop=True)
        insults["sentence"] = (
            "\nInsult: "
            + insults["insult"]
            + "\nSUCCESSFUL answer: "
            + insults["answer"]
            + "\n"
        )
        prompt.add_sentence(f"\n{''.join(insults['sentence'])}")
        prompt.add_sentence(f"\nGenerate a SUCCESSFUL for the following insult:\n")
        prompt.add_sentence(f"\nInsult: {insult}\nSUCCESSFUL answer: ")
        return text_generator.generate_text(prompt.prompt)
