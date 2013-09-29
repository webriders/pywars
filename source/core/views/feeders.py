import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, DetailView
from core.models import Game


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


class GameStateFeed(DetailView):
    model = Game

    def get(self, request, *args, **kwargs):
        game = self.get_object()
        last_round = game.get_last_round()

        state = {
            'state': 'round' if game.is_started() else 'waiting',
            'round': last_round.number if last_round is not None else 0
        }

        return HttpResponse(json.dumps(state), content_type='application/json')

game_state_feed = GameStateFeed.as_view()
