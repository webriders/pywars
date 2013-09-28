from django.shortcuts import redirect
from django.views.generic import FormView, DetailView
from core.forms import StartGameForm
from core.models import Game


class StartGamePage(FormView):
    template_name = 'core/game_creator_page.html'
    form_class = StartGameForm

    def form_valid(self, form):
        game = form.save(self.request)
        return redirect('core-game-page', pk=game.pk)

start_game_page = StartGamePage.as_view()


class GamePage(DetailView):
    template_name = 'core/game_page.html'
    context_object_name = 'game'
    model = Game

game_page = GamePage.as_view()