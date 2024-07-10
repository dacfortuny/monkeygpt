import pandas as pd

from src.mistral_text_generator import MistralTextGenerator
from src.prompts import Prompt
from src.utils import get_insults


class Assault:

    def __init__(self, insult, answer):
        self.insult = insult.insult
        self.answer = answer.answer
        self.successful_insult = False

    def evaluate_insult_success(self):
        text_generator = MistralTextGenerator()

        prompt = Prompt()

        prompt.add_sentence(
            "\nHere you have examples of insults and answers and whether the insult was successful or not:\n-"
        )

        insults = get_insults().sample(frac=1).reset_index(drop=True)
        insults_good = insults[: int(len(insults) / 2)]
        insults_good["sentence"] = insults_good.apply(
            lambda row: f"EXAMPLE>> Insult: {row['insult']} / Answer: {row['answer']} / Success: Yes",
            axis=1,
        )
        insults_bad = insults[int(len(insults) / 2) :]
        insults_bad["answer_shifted"] = insults_bad["answer"].shift(1)
        insults_bad.iloc[0, insults_bad.columns.get_loc("answer_shifted")] = (
            insults_bad.iloc[-1, insults_bad.columns.get_loc("answer")]
        )
        insults_bad["sentence"] = insults_bad.apply(
            lambda row: f"EXAMPLE>> Insult: {row['insult']} / Answer: {row['answer_shifted']} / Success: No",
            axis=1,
        )
        insults = (
            pd.concat([insults_good, insults_bad]).sample(frac=1).reset_index(drop=True)
        )

        prompt.add_sentence("\n- ".join(insults["sentence"].tolist()))
        prompt.add_sentence(
            "\nFollowing these examples, assess whether the following insult-answer pair is succesful or not. Return ONLY 'Yes' or 'No':"
        )
        prompt.add_sentence(
            f"\nInsult: {self.insult} / Answer: {self.answer} / Success: "
        )

        response = text_generator.generate_text(prompt.prompt)

        if response.lower().strip() == "yes":
            self.successful_insult = True

        return self.successful_insult
