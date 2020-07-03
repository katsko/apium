import jrlib
from jrlib import fields


class UserProfile(fields.ObjField):
    first_name = fields.CharField()
    last_name = fields.CharField()
    test = 'abc test'


class SetObjFieldInline(jrlib.Method):
    user_id = fields.IntField(required=True)
    user_profile = UserProfile()
    address = fields.ObjField(
        fields=dict(
            city=fields.CharField(required=True),
            street=fields.CharField()
        ),
        required=False
    )

    def execute(self):
        print('sss')
        print(self.user_profile.first_name)
        print(self.user_profile.last_name)
        print('eee')
        return {
            'user_id': self.user_id,
            'user_profile': {
                'first_name': self.user_profile.first_name,
                'last_name': self.user_profile.last_name,
                'city': self.address.city,
                'street': self.address.street,
            }
        }
