from django.shortcuts import redirect
from django.views.generic import FormView
from core.forms import JoinGameForm
from mixins import PlayerMixin


__all__ = ['join_game_action']


class JoinGameAction(FormView, PlayerMixin):
    form_class = JoinGameForm

    def form_valid(self, form):
        game = form.save(self.get_player_id())
        return redirect('core-game-page', pk=game.pk)

join_game_action = JoinGameAction.as_view()