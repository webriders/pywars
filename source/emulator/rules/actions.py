from emulator.rules.base import Action


class InitialAction(Action):
    duration = 0


class FightingAction(Action):
    pass


class PunchingAction(FightingAction):
    duration = 2
    damage = 5


class KickingAction(FightingAction):
    duration = 4
    damage = 10


class BlockingAction(Action):
    duration = 1


class WaitingAction(Action):
    duration = 1


class GettingHitAction(Action):
    duration = 1


class BlockedAction(Action):
    duration = 0