class PlayerMixin(object):
    """
    Provides utils for working with player object inside views
    """
    def get_player_id(self):
        self.request.session.modified = True
        return self.request.session.session_key