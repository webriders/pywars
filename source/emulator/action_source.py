from emulator.rules import KickingAction, PunchingAction, BlockingAction, WaitingAction


class ValidationError(Exception): pass


class SimpleActionSource(object):
    """
    Very very simple action source, that parses only our commands using regexp
    """

    def __init__(self, code):
        self.code = code
        self._generator_instance = self._generator()

    def _generator(self):
        line_num = 0

        for string in self.code.split('\n'):
            line_num += 1
            string = string.strip()
            if not string or string.startswith('#'):
                continue
            if string == 'player.kick()':
                yield KickingAction()
            elif string == 'player.punch()':
                yield PunchingAction()
            elif string == 'player.block()':
                yield BlockingAction()
            elif string == 'player.wait()':
                yield WaitingAction()
            else:
                raise ValidationError('Unknown command at line %d' % line_num)

    def next(self):
        return self._generator_instance.next()

    def validate(self):
        """
        Validate code
        """
        actions = list(self._generator())
        if len(actions) != 10:
            raise ValidationError('There should be exactly 10 commands')