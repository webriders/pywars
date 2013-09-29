import json
from emulator import PlayerState, GameEmulator
from emulator.action_source import SimpleActionSource
from emulator.rules import FightingRule


class EmulatorService(object):
    """
    Service layer for emulator application
    It gives very simple api to end-user
    """
    def emulate(self, player1_code, player2_code, player1_state_json=None, player2_state_json=None):
        """
        Emulate players with theirs states and codes
        :param player1_code: string with code for player1
        :param player2_code: string with code for player2
        :param player1_state_json: string with JSON state for player1
        :param player2_state_json: string with JSON state for player2
        :return: tuple with JSON of generated scene, JSON of player1 state, JSON of player2 state,
        number of player who won or 0
        """
        player1_action_source = SimpleActionSource(player1_code)
        player2_action_source = SimpleActionSource(player2_code)

        player1 = PlayerState('player1', player1_action_source, player1_state_json)
        player2 = PlayerState('player2', player2_action_source, player2_state_json)

        emulator = GameEmulator([player1, player2], rules=[FightingRule()])

        scene = {}

        def health_callback(player):
            event = {
                'type': 'health',
                'player1': player1.health,
                'player2': player2.health
            }

            scene[emulator.tick] = scene.get(emulator.tick, [])
            scene[emulator.tick].append(event)

        def action_callback(player):
            player_number = 1 if player is player1 else 2

            event = {
                'type': 'frame',
                'player': player_number,
                'state': str(player.action),
                'duration': player.action.duration
            }

            scene[emulator.tick] = scene.get(emulator.tick, [])
            scene[emulator.tick].append(event)

        player1.register_callbacks(health_callback, action_callback)
        player2.register_callbacks(health_callback, action_callback)

        try:
            emulator.run()
        except StopIteration:
            pass

        if player1.health <= 0:
            winner = 2
        elif player2.health <= 0:
            winner = 1
        else:
            winner = 0

        print json.dumps(scene)

        return json.dumps(scene), player1.to_json(), player2.to_json(), winner