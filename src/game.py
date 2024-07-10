import random
import warnings

from src.answers import AnswerPirate, AnswerUser
from src.assault import Assault
from src.insult import Insult
from src.players import Pirate, User

warnings.filterwarnings("ignore")


class Game:
    POINTS_TO_WIN = 3

    def __init__(self, name=None):
        self.user = User(name)
        self.pirate = Pirate()
        self.user_turn = False

    def play(self):
        print(f"\nNEW BATTLE: {self.user.name} vs. {self.pirate.name}")

        while (self.user.score < Game.POINTS_TO_WIN) & (
            self.pirate.score < Game.POINTS_TO_WIN
        ):
            if self.user_turn:
                insult = Insult(input("\nWrite your insult.\n"))
                is_successful_answer = random.getrandbits(1)
                answer = AnswerPirate(insult, is_successful_answer)
                print(f"{self.pirate.name}: {answer.answer}")
                if not is_successful_answer:
                    print(f"\nSuccessful insult!\n")
                    self.user.score = self.user.score + 1
                else:
                    print(f"\nNon successful insult!\n")
                    self.user_turn = not self.user_turn

            else:
                insult = Insult()
                print(f"\n{self.pirate.name}: {insult.insult}")
                answer = AnswerUser(insult)
                assault = Assault(insult, answer)
                is_successful_answer = assault.evaluate_insult_success()
                if not is_successful_answer:
                    print(f"\nSuccessful insult!\n")
                    self.pirate.score = self.pirate.score + 1
                else:
                    print(f"\nNon successful insult!\n")
                    self.user_turn = not self.user_turn

            self.print_score()

        if self.user.score == Game.POINTS_TO_WIN:
            print("\nCONGRATULATIONS, YOU WON!\n")
        else:
            print("\nYOU LOSE, TRY AGAIN!\n")

    def print_score(self):
        print(
            f"Score:\n{self.user.score} {self.user.name}\n{self.pirate.score} {self.pirate.name}"
        )
