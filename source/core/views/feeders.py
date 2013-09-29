import json
from django.http import HttpResponse
from django.views.generic import DetailView
from core.models import Game
from core.views.mixins import PlayerMixin


__all__ = ['new_rounds_feed', 'game_state_feed']


class NewRoundsFeed(DetailView):
    model = Game

    def get(self, request, *args, **kwargs):
        last_round_number = kwargs['last_round_number']
        game = self.get_object()

        game_rounds = game.get_new_rounds(last_round_number)
        rounds = [{'round': game_round.number, 'scene': game_round.scene} for game_round in game_rounds]

        return HttpResponse(json.dumps(rounds), content_type='application/json')

new_rounds_feed = NewRoundsFeed.as_view()


class GameStateFeed(DetailView, PlayerMixin):
    model = Game

    def get(self, request, *args, **kwargs):
        game = self.get_object()
        last_round = game.get_last_round()

        if game.is_finished():
            winner = game.get_result()
            if winner is None:
                winner_player = None
            elif winner.role == Game.ROLE_PLAYER_1:
                winner_player = 1
            else:
                winner_player = 2

            state = {
                'state': 'finished',
                'winner': winner_player
            }
        elif game.is_started():
            state = {
                'state': 'round',
                'current_code': game.get_current_code(self.get_player_id())
            }
        else:
            state = {
                'state': 'waiting'
            }

        players = [game.get_player_1(), game.get_player_2()]

        state.update({
            'round': last_round.number if last_round is not None else 0,
            'players': [players[0].name if players[0] else '...', players[1].name if players[1] else '...']
        })

        return HttpResponse(json.dumps(state), content_type='application/json')

game_state_feed = GameStateFeed.as_view()
