import random

__all__ = ['GameEmulator']


class GameEmulator(object):
    """
    Main object that performs game emulation according to specified rules
    """
    def __init__(self, players, rules):
        """
        :param players: list (with length of 2) of PlayerState instances
        :param rules: list of Rule instances
        """
        assert type(players) is list and len(players) == 2
        assert type(rules) is list and len(rules) >= 1

        self.players = players
        self.rules = rules
        self.tick = 0

    def run(self):
        """
        Run emulator
        """
        self.tick = 0

        while self.tick < 1000 and self.players[0].health > 0 and self.players[1].health > 0:
            # Perform tick
            self.tick += 1
            for player in self.players:
                player.action.tick += 1

            # Perform all queued actions
            for player in self.players:
                player.finish()
                # Queue next action if player has finished action
                if player.action.tick >= player.action.duration:
                    # Need to get next state
                    player.queue_action(player.action_source.next())
                    player.finish()

            # Apply all rules for this tick
            for rule in self.rules:
                # Randomize order for same actions like kick-kick /etc
                player_number = random.randint(0, 1)
                if player_number == 1:
                    rule.resolve(*self.players)
                    rule.resolve(*self.players[::-1])
                else:
                    rule.resolve(*self.players[::-1])
                    rule.resolve(*self.players)