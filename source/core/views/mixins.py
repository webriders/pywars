class PlayerMixin(object):
    """
    Provides utils for working with player object inside views
    """
    def get_player_id(self):
        return self.request.session.session_key