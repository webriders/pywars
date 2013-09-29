from django.views.generic import DetailView
from core.models import Game
from mixins import PlayerMixin, JSONResponseMixin


__all__ = ['new_rounds_feed', 'game_state_feed']


class NewRoundsFeed(DetailView, JSONResponseMixin):
    model = Game

    def get(self, request, *args, **kwargs):
        last_round_number = kwargs['last_round_number']
        game = self.get_object()

        game_rounds = game.get_new_rounds(last_round_number)
        rounds = [{'round': game_round.number, 'scene': game_round.scene} for game_round in game_rounds]

        return self.render_to_json_response(rounds)

new_rounds_feed = NewRoundsFeed.as_view()


class GameStateFeed(DetailView, PlayerMixin, JSONResponseMixin):
    model = Game

    def get(self, request, *args, **kwargs):
        game = self.get_object()
        last_round = game.get_last_round()

        if game.is_finished():
            winner = game.get_result()

            state = {
                'state': 'finished',
                'winner': winner.name if winner else None
            }
        elif game.is_started():
            state = {
                'state': 'round',
                'currentCode': game.get_current_code(self.get_player_id()),
                'isOpponentSubmitted': game.is_opponent_submitted(self.get_player_id())
            }
        else:
            state = {
                'state': 'waiting'
            }

        players = [game.get_player_1(), game.get_player_2()]

        state.update({
            'round': last_round.number if last_round is not None else 0,
            'players': [players[0].name if players[0] else '...', players[1].name if players[1] else '...'],
        })

        return self.render_to_json_response(state)

game_state_feed = GameStateFeed.as_view()
