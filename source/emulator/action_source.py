from emulator.rules import KickingAction, PunchingAction, BlockingAction, WaitingAction


class SimpleActionSource(object):
    """
    Very very simple action source, that parses only our commands using regexp
    """

    def __init__(self, code):
        self.code = code
        self._generator_instance = self._generator()

    def _generator(self):
        for string in self.code.split('\n'):
            string = string.strip()
            if string == 'player.kick()':
                yield KickingAction()
            elif string == 'player.punch()':
                yield PunchingAction()
            elif string == 'player.block()':
                yield BlockingAction()
            elif string == 'player.wait()':
                yield WaitingAction()
            else:
                print 'unknown action'

    def next(self):
        return self._generator_instance.next()