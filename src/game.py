import random
from dataclasses import dataclass
from typing import Optional

from src.answers import AnswerPirate, AnswerUser
from src.assault import Assault
from src.insult import Insult
from src.players import Pirate, User


@dataclass
class RoundResult:
    thrower: str
    insult: str
    answerer: str
    answer: str
    answer_succeeded: bool
    round_winner: str
    game_winner: Optional[str]


class Game:
    POINTS_TO_WIN = 3

    def __init__(self, name=None):
        self.user = User(name=name)
        self.pirate = Pirate()
        self.user_turn = False
        self.winner = None

    def _change_turn(self):
        self.user_turn = not self.user_turn

    def _player(self, kind):
        return self.user if kind == "user" else self.pirate

    def _resolve_round(self, thrower, answer_succeeded):
        # The thrower keeps the upper hand (and scores) only if the answer to
        # their insult fails; a successful comeback flips the attack to them.
        if answer_succeeded:
            round_winner = "pirate" if thrower == "user" else "user"
            self._change_turn()
        else:
            round_winner = thrower
            self._player(thrower).score += 1

        if self.user.score >= Game.POINTS_TO_WIN:
            self.winner = "user"
        elif self.pirate.score >= Game.POINTS_TO_WIN:
            self.winner = "pirate"

        return round_winner

    def throw_pirate_insult(self):
        return Insult()

    def resolve_user_turn(self, insult_text):
        insult = Insult(insult_text)
        answer_succeeded = bool(random.getrandbits(1))
        answer = AnswerPirate(insult, answer_succeeded)
        if answer.is_fallback:
            answer_succeeded = False
        round_winner = self._resolve_round("user", answer_succeeded)
        return RoundResult(
            thrower="user",
            insult=insult.insult,
            answerer="pirate",
            answer=answer.answer,
            answer_succeeded=answer_succeeded,
            round_winner=round_winner,
            game_winner=self.winner,
        )

    def resolve_pirate_turn(self, insult, answer_text):
        answer = AnswerUser(insult, answer_text)
        assault = Assault(insult, answer)
        answer_succeeded = assault.evaluate_insult_success()
        round_winner = self._resolve_round("pirate", answer_succeeded)
        return RoundResult(
            thrower="pirate",
            insult=insult.insult,
            answerer="user",
            answer=answer.answer,
            answer_succeeded=answer_succeeded,
            round_winner=round_winner,
            game_winner=self.winner,
        )

    def play(self):
        print(f"\nNEW BATTLE: {self.user.name} vs. {self.pirate.name}")

        while self.winner is None:
            if self.user_turn:
                result = self.resolve_user_turn(input("\nWrite your insult.\n"))
                print(f"{self.pirate.name}: {result.answer}")
            else:
                insult = self.throw_pirate_insult()
                print(f"\n{self.pirate.name}: {insult.insult}")
                result = self.resolve_pirate_turn(insult, input("Write your answer.\n"))

            if result.round_winner == result.thrower:
                print("\nSuccessful insult!\n")
            else:
                print("\nUnsuccessful insult!\n")

            self.print_score()

        if self.winner == "user":
            print("\nCONGRATULATIONS, YOU WON!\n")
        else:
            print("\nYOU LOSE, TRY AGAIN!\n")

    def print_score(self):
        print(
            f"Score:\n{self.user.score} {self.user.name}"
            f"\n{self.pirate.score} {self.pirate.name}"
        )
