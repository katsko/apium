import jrlib
from jrlib import fields


class UserProfile(fields.ObjField):
    first_name = fields.CharField(required=True)
    # first_name = fields.CharField()
    last_name = fields.CharField()


class SetObjFieldRequired(jrlib.Method):
    user_id = fields.IntField(required=True)
    # user_profile = UserProfile(required=True)
    user_profile = UserProfile()

    def execute(self):
        return {
            'user_id': self.user_id,
        }
