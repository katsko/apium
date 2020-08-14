import jrlib
from jrlib import jf


USERS = [('u1', 'p1'), ('u2', 'p2')]


class LoginUser(jrlib.Method):

    username = jf.Str(required=True)
    password = jf.Str(required=True)

    def execute(self):
        is_success = (self.username, self.password) in USERS
        self.response.set_cookie('is_auth', is_success)
        return {'login_success': is_success}
