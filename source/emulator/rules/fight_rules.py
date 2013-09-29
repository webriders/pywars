from emulator.rules.base import Rule
from emulator.rules.actions import *


__all__ = ['FightingRule', 'VictoryRule']


class FightingRule(Rule):
    """
    Simple rules for performing fighting operations
    """
    def resolve(self, player, enemy):
        if isinstance(player.action, FightingAction):
            # Perform energy changing
            if type(player.action) is PunchingAction:
                player.queue_energy(player.energy-20)
            elif type(player.action) is KickingAction:
                player.queue_energy(player.energy-40)

            if isinstance(enemy.action, BlockingAction):
                return  # Enemy blocked hit

            # Hit is not blocked
            if type(player.action) is PunchingAction:
                enemy.queue_action(GettingHitByPunchAction())
            elif type(player.action) is KickingAction:
                enemy.queue_action(GettingHitByKickAction())

            # Decrease healths
            enemy.queue_damage(player.action.damage)

            # Enemy died
            if enemy.health <= 0:
                if type(player.action) is PunchingAction:
                    enemy.queue_action(FallingByPunchAction())
                elif type(player.action) is KickingAction:
                    enemy.queue_action(FallingByKickAction())


class VictoryRule(Rule):
    """
    Rule for changing players action to VictoryAction
    """
    def resolve(self, player, enemy):
        if isinstance(player.action, FallingAction) and enemy.action != enemy._queued_action:
            enemy.queue_action(VictoryAction())