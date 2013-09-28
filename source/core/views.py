from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
from core.forms import StartGameForm, JoinGameForm
from core.models import Game


class PlayerMixin(object):
    """
    Provides utils for working with player object inside views
    """
    def get_player_id(self):
        self.request.session.modified = True
        return self.request.session.session_key


class StartGamePage(FormView, PlayerMixin):
    """
    The first step in the game workflow
    """
    template_name = 'core/game_creator_page.html'
    form_class = StartGameForm

    def form_valid(self, form):
        game = form.save(self.get_player_id())
        return redirect('core-game-page', pk=game.pk)

start_game_page = StartGamePage.as_view()


class JoinGameFeeder(FormView, PlayerMixin):
    form_class = JoinGameForm

    def form_valid(self, form):
        game = form.save(self.get_player_id())
        return redirect('core-game-page', pk=game.pk)

join_game_feeder = JoinGameFeeder.as_view()


class GamePage(DetailView, PlayerMixin):
    """
    Page with game scene
    """
    template_name = 'core/game_page.html'
    context_object_name = 'game'
    model = Game

    def get_context_data(self, **kwargs):
        context = super(GamePage, self).get_context_data(**kwargs)
        game = self.get_object()
        context.update({
            'user_role': game.get_role_for(self.get_player_id()),
            'join_game_form': JoinGameForm(initial={'game': game})
        })

        return context

game_page = GamePage.as_view()import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from core.models import Game


class NewRoundsView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        # Mock now
        import os
        mock_path = os.path.join(os.path.dirname(__file__), 'mocks/scene.json')
        return HttpResponse(open(mock_path).read(), content_type='application/json')

        #game_pk = kwargs['game_pk']
        #last_round_number = kwargs['last_round_number']
        #game = get_object_or_404(Game, pk=game_pk)

        #game_rounds = game.get_new_rounds(last_round_number)
        #rounds = [{'round': game_round.number, 'scene': game_round.scene} for game_round in game_rounds]

        #return HttpResponse(json.dumps(rounds), content_type='application/json')

new_rounds_feed = NewRoundsView.as_view()