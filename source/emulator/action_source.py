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
            print 'executing %s' % string
            string = string.strip()
            if string == 'kick()':
                yield KickingAction()
            elif string == 'punch()':
                yield PunchingAction()
            elif string == 'block()':
                yield BlockingAction()
            elif string == 'wait()':
                yield WaitingAction()
            else:
                print 'unknown action'

    def next(self):
        return self._generator_instance.next()