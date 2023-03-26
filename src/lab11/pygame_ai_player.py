import random
from lab11.turn_combat import CombatPlayer


""" Create PyGameAIPlayer class here"""


class PyGameAIPlayer:
    def __init__(self) -> None:
        pass
    
    def selectAction(self, state):
        return ord(str(state.current_city + 1))


""" Create PyGameAICombatPlayer class here"""


class PyGameAICombatPlayer(CombatPlayer):
    def __init__(self, name):
        super().__init__(name)
    
    def weapon_selecting_strategy(self):
        choice = random.randint(1, 3)
        self.weapon = choice - 1
        return self.weapon
