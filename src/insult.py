from random import shuffle

from src.mistral_text_generator import MistralTextGenerator
from src.prompts import Prompt
from src.utils import get_insults


class Insult:

    def __init__(self, text_input=None):
        self.insult = text_input or self._generate_insult()

    def _generate_insult(self):
        text_generator = MistralTextGenerator()
        prompt = Prompt()
        prompt.add_sentence("\nHere you have examples of the insults used in the game:\n-")
        insults = get_insults()["insult"].tolist()
        shuffle(insults)
        prompt.add_sentence("\n- ".join(insults))
        prompt.add_sentence(
            "\nBased on this, generate ONE new insult that could fit in the game. Return ONLY the generated insult.")
        return text_generator.generate_text(prompt.prompt)
