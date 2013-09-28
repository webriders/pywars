from django import forms
from core.models import Game


class StartGameForm(forms.Form):
    """
    Processes information about game configuration and first player (who creates the game)
    """
    player_username = forms.CharField(max_length=254)

    def save(self, player_id):
        """
        :param player_id: Who does create game?
        :type player_id: basestring
        """
        new_game = Game.objects.create()
        new_game.join_game(player_id, self.cleaned_data['player_username'])
        return new_game
