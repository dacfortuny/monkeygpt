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
        self.user = User(name=name)
        self.pirate = Pirate()
        self.user_turn = False

    def _change_turn(self):
        self.user_turn = not self.user_turn

    def play(self):
        print(f"\nNEW BATTLE: {self.user.name} vs. {self.pirate.name}")

        while True:
            if self.user_turn:
                insult = Insult(input("\nWrite your insult.\n"))
                is_successful_answer = random.getrandbits(1)
                answer = AnswerPirate(insult, is_successful_answer)
                print(f"{self.pirate.name}: {answer.answer}")
                if not is_successful_answer:
                    print("\nSuccessful insult!\n")
                    self.user.score += 1
                else:
                    print("\nUnsuccessful insult!\n")
                    self._change_turn()

            else:
                insult = Insult()
                print(f"\n{self.pirate.name}: {insult.insult}")
                answer = AnswerUser(insult)
                assault = Assault(insult, answer)
                is_successful_answer = assault.evaluate_insult_success()
                if not is_successful_answer:
                    print("\nSuccessful insult!\n")
                    self.pirate.score += 1
                else:
                    print("\nUnsuccessful insult!\n")
                    self._change_turn()

            self.print_score()

            if self.user.score == Game.POINTS_TO_WIN:
                print("\nCONGRATULATIONS, YOU WON!\n")
                break

            if self.pirate.score == Game.POINTS_TO_WIN:
                print("\nYOU LOSE, TRY AGAIN!\n")
                break

    def print_score(self):
        print(
            f"Score:\n{self.user.score} {self.user.name}"
            f"\n{self.pirate.score} {self.pirate.name}"
        )
