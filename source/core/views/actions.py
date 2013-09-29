from django.shortcuts import redirect
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from core.exceptions import GameException
from core.forms import JoinGameForm, SubmitCodeForm
from core.models import Game
from mixins import PlayerMixin, JSONResponseMixin


__all__ = ['join_game_action', 'submit_code_action']


class JoinGameAction(FormView, PlayerMixin):
    form_class = JoinGameForm

    def form_valid(self, form):
        game = form.save(self.get_player_id())
        return redirect('core-game-page', pk=game.pk)

join_game_action = JoinGameAction.as_view()


class SubmitCodeAction(FormView, PlayerMixin, SingleObjectMixin, JSONResponseMixin):
    model = Game
    form_class = SubmitCodeForm

    def form_valid(self, form):
        game = self.get_object()
        try:
            form.save(game, self.get_player_id())
        except GameException, exc:
            return self.render_to_json_response({
                'status': 'error',
                'message': exc.message
            })

        return self.render_to_json_response({'status': 'success'})

    def form_invalid(self, form):
        return self.render_to_json_response({
            'status': 'error',
            'message': u"You have to enter some code"
        })

submit_code_action = SubmitCodeAction.as_view()