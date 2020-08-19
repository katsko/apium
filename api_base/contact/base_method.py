import jrlib
from jrlib import jf


def valid_user_ids(value):
    if value not in [1, 2, 3]:
        raise ValueError("Value must be 1, 2 or 3")


class BaseContact(jrlib.Method):
    user_id = jf.Int(validators=[valid_user_ids])
    comment = jf.Str()

    def validate(self):
        super(BaseContact, self).validate()
        if not self.comment or len(self.comment) != self.user_id:
            raise ValueError("Error comment lenght")
