from random import sample

from src.mistral_text_generator import MistralTextGenerator
from src.prompts import Prompt
from src.utils import get_insults

N_EXAMPLE_INSULTS = 8


class Insult:
    def __init__(self, text_input=None):
        self.insult = text_input or self._generate_insult()

    def _generate_insult(self):
        text_generator = MistralTextGenerator()
        prompt = Prompt()
        prompt.add_sentence("\nHere you have examples of the insults used in the game:\n-")
        all_insults = get_insults()["insult"].tolist()
        insults = sample(all_insults, min(N_EXAMPLE_INSULTS, len(all_insults)))
        prompt.add_sentence("\n- ".join(insults))
        prompt.add_sentence(
            "\nBased on this, generate ONE new insult that could fit in the game. "
            "Avoid overused 'your mother' jokes and overused pirate clichés like "
            "'barnacles' or 'scurvy'; favor other classic pirate insult themes "
            "(cowardice, appearance, smell, fighting skill, wit, etc.) and vary the "
            "vocabulary each time. Return ONLY the generated insult."
        )
        return text_generator.generate_text(prompt.prompt)
