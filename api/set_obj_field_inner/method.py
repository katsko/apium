import jrlib
from jrlib import jf


class SubUserProfile(jf.Obj):

    class SubSub(jf.Obj):

        class PhoneField(jf.Str):
            def validate(self):
                if self.value and len(self.value) < 3:
                    raise ValueError(
                        'Phone is too short, required 3 or more symbols')

        email = jf.Str()
        phone = PhoneField()
        address = jf.Str(required=True)

        def validate(self):
            if not (self.email or self.phone):
                raise ValueError('Required email or phone')

    age = jf.Int()
    gender = jf.Int(required=True)
    card = SubSub(required=True)


class UserProfile(jf.Obj):
    first_name = jf.Str(required=True)
    last_name = jf.Str()
    sub = SubUserProfile(required=True)
    test = 'abc test'


class SetObjFieldInner(jrlib.Method):
    user_id = jf.Int(required=True)
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
