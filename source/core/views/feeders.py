import json
from django.http import HttpResponse
from django.views.generic import View, DetailView
from core.models import Game


__all__ = ['new_rounds_feed', 'game_state_feed']


class NewRoundsFeed(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # Mock now
        import os
        mock_path = os.path.join(os.path.dirname(__file__), '../mocks/scene.json')
        return HttpResponse(open(mock_path).read(), content_type='application/json')

        #game_pk = kwargs['game_pk']
        #last_round_number = kwargs['last_round_number']
        #game = get_object_or_404(Game, pk=game_pk)

        #game_rounds = game.get_new_rounds(last_round_number)
        #rounds = [{'round': game_round.number, 'scene': game_round.scene} for game_round in game_rounds]

        #return HttpResponse(json.dumps(rounds), content_type='application/json')

new_rounds_feed = NewRoundsFeed.as_view()


class GameStateFeed(DetailView):
    model = Game

    def get(self, request, *args, **kwargs):
        game = self.get_object()

        state = {
            'state': 'round' if game.is_started() else 'waiting',
            'round': 0
        }

        return HttpResponse(json.dumps(state), content_type='application/json')

game_state_feed = GameStateFeed.as_view()
