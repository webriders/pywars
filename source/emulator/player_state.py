import json
from emulator.rules import Action, InitialAction


__all__ = ['PlayerState']


class PlayerState(object):
    def __init__(self, name, action_source, json=None):
        """
        :param name: string with player's name (useful for debug)
        :param action_source: generator instance, that will be used to get actions for player
        :param json: is specified load state from JSON
        """
        assert type(name) in (str, unicode)
        assert hasattr(action_source, 'next')

        self.name = name
        self.action_source = action_source
        self.action = InitialAction()
        self.health = 100
        self.energy = 100
        self._queued_action = None
        self._queued_health = None
        self._queued_energy = None
        self._health_callback = None
        self._energy_callback = None
        self._action_callback = None

        if json is not None:
            self.from_json(json)

    def __str__(self):
        return self.name

    def from_json(self, json_data):
        """
        Reload state from JSON
        :param json: string with valid JSON data
        """
        assert type(json_data) in (str, unicode)

        data = json.loads(json_data)
        self.health = data['health']
        self.energy = data['energy']

    def to_json(self):
        """
        Serialize state to json
        """
        return json.dumps({'health': self.health, 'energy': self.energy})

    def register_callbacks(self, health_callback, energy_callback, action_callback):
        """
        Add callbacks that will be called when state is changed
        :param health_callback: callable that will be called on health changes
        :param action_callback: callable that will be called on action changes
        """
        self._health_callback = health_callback
        self._energy_callback = energy_callback
        self._action_callback = action_callback

    def queue_damage(self, value):
        """
        Tell to change health value (health-value)
        :param value: number of points to decrease from health
        """
        assert type(value) is int

        if self.health - value < 0:
            value = self.health

        self.health = self._queued_health = self.health - value

    def queue_energy(self, value):
        """
        Tell to change energy value
        :param value: next value of energy
        """
        assert type(value) is int

        if value > 100:
            value = 100

        if value < 0:
            value = 0

        self.energy = self._queued_energy = value

    def queue_action(self, action):
        """
        Tell what action to perform in next tick
        :param action: Action instance
        """
        assert isinstance(action, Action)

        self.action = self._queued_action = action

    def finish(self):
        """
        Emit events for all queued operations
        """
        if self._queued_health is not None:
            if self._health_callback is not None:
                self._health_callback(self)

        if self._queued_energy is not None:
            if self._energy_callback is not None:
                self._energy_callback(self)

        if self._queued_action is not None:
            if self._action_callback is not None:
                self._action_callback(self)

        self._queued_health = None
        self._queued_energy = None
        self._queued_action = None