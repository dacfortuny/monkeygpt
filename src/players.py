class Player:
    def __init__(self, name, type):
        self.name = name
        self.type = type


class User(Player):
    def __init__(self, name):
        super().__init__(name, type="user")


class Pirate(Player):
    def __init__(self, name):
        super().__init__(name, type="pirate")
