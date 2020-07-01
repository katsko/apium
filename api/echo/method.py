import jrlib
from jrlib import fields
# from jrlib import middleware  # пока этого нет

# TODO: можно добавлять декоратор, в котором параметр - это
# абстрактный апи-метод, т.к. метод, который сам не вызывается в чистом виде
# но используется как декоратор, чтобы вызвались его validate()


# @middleware(Logger)
# @middleware(Auth)

class Echo(jrlib.Method):
    msg = fields.CharField(required=True)

    def validate(self):
        print('11111111111')
        super(Echo, self).validate()
        if self.msg == '222':
            raise ValueError('error 222!!!!')
        print('22222222222')

    def execute(self):
        return self.msg
