from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _


class Game(models.Model):
    """
    Information about game
    """
    time_started = models.DateTimeField(verbose_name=_("Start time"), null=True, blank=True)
    time_ended = models.DateTimeField(verbose_name=_("End time"), null=True, blank=True)

    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")

    def join_game(self, player_id, name):
        """
        Join to game with specified player ID and name
        :param player_id: string containing player ID
        :param name: player name
        :return: Player instance
        """
        try:
            return Player.objects.get(game=self, ident=player_id)  # Already joined as player, just return player
        except Player.DoesNotExist:
            pass

        players_count = self.players.count()

        if players_count == 0:
            # First player
            return Player.objects.create(game=self, ident=player_id, role=Player.ROLE_PLAYER_1, name=name)
        elif players_count == 1:
            # Second player
            return Player.objects.create(game=self, ident=player_id, role=Player.ROLE_PLAYER_2, name=name)
        else:
            raise Exception('Game is already started')

    def is_game_started(self):
        """
        Check if game is started.
        Game considered to be started when there are 2 joined players with filled names
        :return: True if game is started
        """
        return self.players.filter().count() == 2

    def get_new_rounds(self, last_round_number):
        """
        Get new Round instances since last round number
        :param last_round_number: last round number, that client has
        :return: QuerySet of Round instances ordered by their number
        """
        return self.rounds.filter(number__gt=last_round_number)

    def submit_code(self, player_id, code):
        """
        Submit code for current round
        :param player_id: string containing player ID
        :param code: string containing code
        """
        if self.is_game_started() is False:
            raise Exception('Game is not started')

        try:
            player = self.players.get(ident=player_id)
        except Player.DoesNotExist:
            raise Exception('Unknown player specified')

        current_round = self.rounds.all().order_by('-number')[0]
        try:
            GameSnippet.objects.create(game_round=current_round, player=player, code=code)
        except IntegrityError:
            raise Exception('Code for this round was already submitted')


class Player(models.Model):
    """
    Information about player id and his state
    """
    ROLE_PLAYER_1 = 'player1'
    ROLE_PLAYER_2 = 'player2'

    ROLE_CHOICES = (
        (ROLE_PLAYER_1, "Player 1"),
        (ROLE_PLAYER_2, "Player 2")
    )

    game = models.ForeignKey('Game', verbose_name=_("Game"), related_name="+")
    ident = models.CharField(verbose_name=_("Player ID"), max_length=254)
    name = models.CharField(verbose_name=_("Name"), max_length=254)

    role = models.CharField(verbose_name=_("Role"), max_length=16, choices=ROLE_CHOICES)
    health = models.IntegerField(default=100)

    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")
        unique_together = ('game', 'role')  # There can be only one role per game


class GameRound(models.Model):
    """
    Information about game round
    """
    game = models.ForeignKey('Game', verbose_name=_("Game"), related_name='rounds')
    number = models.IntegerField(verbose_name=_("Round number"))
    scene = models.TextField(verbose_name=_("Scene data"), null=True, blank=True)

    class Meta:
        verbose_name = _("Game round")
        verbose_name_plural = _("Game rounds")
        ordering = ('number',)


class GameSnippet(models.Model):
    """
    Code snippet uploaded by player for specified game
    """
    game_round = models.ForeignKey('GameRound', verbose_name=_("Game round"), related_name='snippets')
    player = models.ForeignKey('Player', verbose_name=_("Player"), related_name='snippets')
    code = models.TextField(verbose_name=_("Code"))

    class Meta:
        verbose_name = _("Code snippet")
        verbose_name_plural = _("Code snippets")
        unique_together = ('game_round', 'player',)  # There should be one snippet within round per player