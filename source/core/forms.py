from django import forms
from core.models import Game


class JoinGameForm(forms.Form):
    """
    Process information about second player
    """
    game = forms.ModelChoiceField(Game.objects.all(), widget=forms.HiddenInput, required=False)
    player_username = forms.CharField(max_length=254)

    def save(self, player_id):
        """
        :param player_id: Who does join game?
        :type player_id: basestring
        """
        game = self.cleaned_data.get('game')
        if game is None:
            game = Game.objects.create()
        game.join_game(player_id, self.cleaned_data['player_username'])
        return game


class SubmitCodeForm(forms.Form):
    """
    Process submitted code from player
    """
    code = forms.CharField(widget=forms.Textarea)

    def save(self, game, player_id):
        """
        :param game: For what game this code?
        :type game: Game instance
        :param player_id: Who does submit code?
        :type player_id: basestring
        """
        game.submit_code(player_id, self.cleaned_data['code'])
