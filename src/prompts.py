from src.players import get_pirate_types
from src.utils import get_game_overview, load_conf, read_txt_file


class Prompt:
    def __init__(self):
        self.prompt = get_game_overview()

    def add_sentence(self, sentence: str):
        self.prompt = f"{self.prompt} {sentence}"


def prompt_for_pirate_types_generator(n: int = 50):
    prompt = Prompt()
    pirate_types = get_pirate_types(subsets=["original"], as_string=True)
    sentence = read_txt_file(
        load_conf()["PATH_TO_PROMPT_GENERATE_PIRATE_TYPES"]
    ).format(pirate_types=pirate_types, n=n)
    prompt.add_sentence(sentence)
    return prompt.prompt


def prompt_for_insult_generator(n: int=50):
    prompt = Prompt()
    pirate_types = get_pirate_types(subsets=["original"], as_string=True)
    sentence = read_txt_file(
        load_conf()["PATH_TO_PROMPT_GENERATE_PIRATE_TYPES"]
    ).format(pirate_types=pirate_types, n=n)
    prompt.add_sentence(sentence)
    return prompt.prompt
