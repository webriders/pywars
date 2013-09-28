from django import forms
from core.models import Game


class StartGameForm(forms.Form):
    """
    Processes information about game configuration and first player (who creates the game)
    """
    player_username = forms.CharField(max_length=254)

    def save(self, request):
        """
        :params request: Django request object
        :type request: HttpRequest
        """
        new_game = Game.objects.create()
        new_game.join_game(request.session.session_key, self.cleaned_data['player_username'])
        return new_game
