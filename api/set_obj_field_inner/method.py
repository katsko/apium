import jrlib
from jrlib import fields


class SubUserProfile(fields.ObjField):

    class SubSub(fields.ObjField):

        class PhoneField(fields.CharField):
            def validate(self):
                if self.value and len(self.value) < 3:
                    raise ValueError(
                        'Phone is too short, required 3 or more symbols')

        email = fields.CharField()
        phone = PhoneField()
        address = fields.CharField(required=True)

        def validate(self):
            if not (self.email or self.phone):
                raise ValueError('Required email or phone')

    age = fields.IntField()
    gender = fields.IntField(required=True)
    card = SubSub(required=True)


class UserProfile(fields.ObjField):
    first_name = fields.CharField(required=True)
    last_name = fields.CharField()
    sub = SubUserProfile(required=True)
    test = 'abc test'


class SetObjFieldInner(jrlib.Method):
    user_id = fields.IntField(required=True)
    user_profile = UserProfile(required=True)

    def execute(self):
        print('sss')
        print(self.user_profile.first_name)
        print(self.user_profile.last_name)
        print('eee')
        print(self.user_profile.sub.age)
        print('eee sub')
        return {
            'user_id': self.user_id,
            'user_profile': {
                'first_name': self.user_profile.first_name,
                'last_name': self.user_profile.last_name,
                'value': self.user_profile.value,
                'required': self.user_profile.required,
            }
        }
