import csv
import re
from pathlib import Path
from random import sample

from src.mistral_text_generator import MistralTextGenerator
from src.prompts import Prompt
from src.utils import get_insult_cache_path, get_insults

N_EXAMPLE_INSULTS = 20
CACHE_SIZE = 30

LIST_MARKER = re.compile(r"^\s*(?:[-*]|\d+[.)])\s*")


class Insult:
    def __init__(self, text_input=None):
        self.insult = text_input or self._get_insult()

    def _get_insult(self):
        cache = self._load_cache()
        if not cache:
            cache = self._generate_insult_cache()
        insult = cache.pop(0)
        self._save_cache(cache)
        return insult

    def _load_cache(self):
        cache_path = Path(get_insult_cache_path())
        if not cache_path.exists():
            return []
        with open(cache_path, newline="") as file:
            return [row[0] for row in csv.reader(file) if row]

    def _save_cache(self, cache):
        cache_path = Path(get_insult_cache_path())
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([insult] for insult in cache)

    def _generate_insult_cache(self):
        text_generator = MistralTextGenerator()
        prompt = Prompt()
        prompt.add_sentence("\nHere you have examples of the insults used in the game:\n-")
        all_insults = get_insults()["insult"].tolist()
        examples = sample(all_insults, min(N_EXAMPLE_INSULTS, len(all_insults)))
        prompt.add_sentence("\n- ".join(examples))
        prompt.add_sentence(
            f"\nBased on this, generate {CACHE_SIZE} new insults that could fit in the game. "
            "Avoid overused 'your mother' jokes and overused pirate clichés like "
            "'barnacles' or 'scurvy'; favor other classic pirate insult themes "
            "(cowardice, appearance, smell, fighting skill, wit, etc.) and vary the "
            f"vocabulary. Make sure there is real variety among the {CACHE_SIZE} insults: "
            "don't repeat the same theme, sentence structure, or phrasing twice. "
            "Return ONLY the insults, one per line, with no numbering, bullets, or "
            "extra commentary."
        )
        response = text_generator.generate_text(prompt.prompt)
        return self._parse_insults(response)

    @staticmethod
    def _parse_insults(response):
        lines = (LIST_MARKER.sub("", line).strip() for line in response.splitlines())
        return [line for line in lines if line]
