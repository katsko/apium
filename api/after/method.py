import jrlib
from jrlib import jf


class Auth(jrlib.Method):
    username = jf.Str()
    password = jf.Str()

    def __middle(self):
        print('mm')
        token = self.request.META.get('HTTP_X_AUTHENTICATION')
        if not token and not (self.username == 'u' and self.password == 'p'):
            raise ValueError('Access denied')

    def __after(self):
        self.result.extend({'user_hash': 'abc'})


class Middle(Auth):
    msg = jf.Str()

    def execute(self):
        print('ee')
        return {'msg': self.msg}
