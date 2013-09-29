from django.db import models, IntegrityError, transaction
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from core.exceptions import GameException
from emulator.services.emulator_service import EmulatorService


class Game(models.Model):
    """
    Information about game
    """
    ROLE_PLAYER_1 = 'player1'
    ROLE_PLAYER_2 = 'player2'
    ROLE_OBSERVER = 'observer'

    MAX_ROUNDS_COUNT = 12

    time_started = models.DateTimeField(verbose_name=_("Start time"), null=True, blank=True)
    time_finished = models.DateTimeField(verbose_name=_("End time"), null=True, blank=True)

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
        players_count = self.players.count()

        if players_count == 0:
            self.players.create(game=self, ident=player_id, role=Game.ROLE_PLAYER_1, name=name)
        elif players_count == 1:
            self.players.create(game=self, ident=player_id, role=Game.ROLE_PLAYER_2, name=name)
            GameRound.objects.create(game=self, number=1)
            self.time_started = timezone.now()
            self.save()
        else:
            raise GameException('Game is already started')

    def get_role_for(self, player_id):
        """
        Returns role for par
        """
        try:
            return self.players.get(ident=player_id).role
        except Player.DoesNotExist:
            pass

        players_count = self.players.count()

        if players_count == 0:
            return self.ROLE_PLAYER_1
        elif players_count == 1:
            return self.ROLE_PLAYER_2

        return self.ROLE_OBSERVER

    def get_player_1(self):
        try:
            return self.players.get(role=Game.ROLE_PLAYER_1)
        except Player.DoesNotExist:
            pass

    def get_player_2(self):
        try:
            return self.players.get(role=Game.ROLE_PLAYER_2)
        except Player.DoesNotExist:
            pass

    def is_started(self):
        """
        Check if game is started.
        :return: True if game is started
        """
        return self.time_started is not None

    def is_finished(self):
        """
        Check if games is ended
        :return: True if game is ended
        """
        return self.time_ended is not None

    def get_result(self):
        """
        Get game result
        :return: Player instance if there is winner,
        None if game was played in draw,
        raise exception if game is not finished
        """
        if not self.is_finished():
            raise GameException('Game is not finished')

        try:
            return self.players.get(is_winner=True)
        except Player.DoesNotExist:
            return None

    def get_new_rounds(self, last_round_number):
        """
        Get new Round instances since last round number
        :param last_round_number: last round number, that client has
        :return: QuerySet of Round instances ordered by their number
        """
        return self.rounds.filter(number__gt=last_round_number, scene__isnull=False)

    def get_last_round(self):
        """
        Get last Round instance that has state
        :return: Round instance
        """
        if not self.is_started():
            raise GameException('Game is not started')

        return self.rounds.filter(state__isnull=False).order_by('-number')[0]

    def submit_code(self, player_id, code):
        """
        Submit code for current round
        :param player_id: string containing player ID
        :param code: string containing code
        """
        if self.is_started() is False:
            raise GameException('Game is not started')

        try:
            player = self.players.get(ident=player_id)
        except Player.DoesNotExist:
            raise GameException('Unknown player specified')

        current_round = self.rounds.all().order_by('-number')[0]
        try:
            GameSnippet.objects.create(game_round=current_round, player=player, code=code)
        except IntegrityError:
            raise GameException('Code for this round was already submitted')


class Player(models.Model):
    """
    Information about player id and his state
    """
    ROLE_CHOICES = (
        (Game.ROLE_PLAYER_1, "Player 1"),
        (Game.ROLE_PLAYER_2, "Player 2")
    )

    game = models.ForeignKey('Game', verbose_name=_("Game"), related_name="players")
    ident = models.CharField(verbose_name=_("Player ID"), max_length=254)
    name = models.CharField(verbose_name=_("Name"), max_length=254)

    role = models.CharField(verbose_name=_("Role"), max_length=16, choices=ROLE_CHOICES)
    state = models.TextField(verbose_name=_("State"), null=True, blank=True)
    is_winner = models.BooleanField(verbose_name=_("Is winner?"), default=False)

    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")
        unique_together = ('game', 'role')  # There can be only one role per game

    def __unicode__(self):
        return self.name


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
    Code snippet uploaded by player for specified game round
    """
    game_round = models.ForeignKey('GameRound', verbose_name=_("Game round"), related_name='snippets')
    player = models.ForeignKey('Player', verbose_name=_("Player"), related_name='snippets')
    code = models.TextField(verbose_name=_("Code"))

    class Meta:
        verbose_name = _("Code snippet")
        verbose_name_plural = _("Code snippets")
        unique_together = ('game_round', 'player',)  # There should be one snippet within round per player


@transaction.commit_on_success
def emulate_round(sender, **kwargs):
    """
    Emulate code if all snippets for round was submitted
    """
    game_round = kwargs['instance'].game_round
    game = game_round.game

    if game_round.snippets.count() == 2:
        service = EmulatorService()

        player1 = game.get_player_1()
        player1_code = game_round.snippets.get(player=player1)

        player2 = game.get_player_2()
        player2_code = game_round.snippets.get(player=player2)

        game_round.scene, player1.state, player2.state, winner = \
            service.emulate(player1_code, player2_code, player1.state, player2.state)

        if winner > 0 or game_round.number >= Game.MAX_ROUNDS_COUNT:
            if winner == 1:
                player1.is_winner = True
            elif winner == 2:
                player2.is_winner = True

            game.time_finished = timezone.now()
        else:
            GameRound.objects.create(game=game_round.game, number=game_round.number+1)

        game_round.save()
        game.save()
        player1.save()
        player2.save()

post_save.connect(emulate_round, sender=GameSnippet)