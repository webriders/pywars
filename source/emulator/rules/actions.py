from emulator.rules.base import Action


class InitialAction(Action):
    name = 'initial'
    duration = 0


class FightingAction(Action):
    pass


class PunchingAction(FightingAction):
    name = 'punching'
    duration = 1
    damage = 5


class KickingAction(FightingAction):
    name = 'kicking'
    duration = 1
    damage = 10


class BlockingAction(Action):
    name = 'blocking'
    duration = 1


class WaitingAction(Action):
    name = 'waiting'
    duration = 1


class GettingHitByPunchAction(Action):
    name = 'being_hit_by_punch'
    duration = 1


class GettingHitByKickAction(Action):
    name = 'being_hit_by_kick'
    duration = 1


class FallingAction(Action):
    duration = 1

class FallingByPunchAction(FallingAction):
    name = 'falling_by_punch'


class FallingByKickAction(FallingAction):
    name = 'falling_by_kick'


class VictoryAction(Action):
    duration = 1
    name = 'victory'