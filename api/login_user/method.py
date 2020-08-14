import jrlib
from jrlib import jf
from storage.data import USERS


class LoginUser(jrlib.Method):

    username = jf.Str(required=True, nullable=False)
    password = jf.Str(required=True, nullable=False)

    def execute(self):
        user = USERS.get(self.username)
        is_success = False
        if user:
            is_success = user.get("password") == self.password
        self.response.set_cookie("is_auth", is_success)
        return {"login_success": is_success}
