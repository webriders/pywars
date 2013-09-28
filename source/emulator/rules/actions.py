from emulator.rules.base import Action


class InitialAction(Action):
    name = 'initial'
    duration = 0


class FightingAction(Action):
    pass


class PunchingAction(FightingAction):
    name = 'punching'
    duration = 2
    damage = 5


class KickingAction(FightingAction):
    name = 'kicking'
    duration = 4
    damage = 10


class BlockingAction(Action):
    name = 'blocking'
    duration = 1


class WaitingAction(Action):
    name = 'waiting'
    duration = 1


class GettingHitAction(Action):
    name = 'being_hit'
    duration = 1


class BlockedAction(Action):
    duration = 0