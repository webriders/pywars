from emulator.rules.base import Rule
from emulator.rules.actions import *


__all__ = ['FightingRule']


class FightingRule(Rule):
    """
    Simple rules for performing fighting operations
    """
    def resolve(self, player, enemy):
        if isinstance(player.action, FightingAction):
            if type(player.action) is PunchingAction:
                player.queue_energy(player.energy-20)
            elif type(player.action) is KickingAction:
                player.queue_energy(player.energy-40)

            if isinstance(enemy.action, BlockingAction):
                print '%s blocked hit' % enemy
                return  # Enemy blocked hit

            # Hit is not blocked
            print "%s received damage %d" % (enemy, player.action.damage)
            if type(player.action) is PunchingAction:
                enemy.queue_action(GettingHitByPunchAction())
            elif type(player.action) is KickingAction:
                enemy.queue_action(GettingHitByKickAction())
            enemy.finish()

            enemy.queue_damage(player.action.damage)