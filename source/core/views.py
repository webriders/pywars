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

game_page = GamePage.as_view()