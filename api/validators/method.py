import jrlib
from jrlib import jf


class LastName(jf.Str):
    def validate(self):
        super(LastName, self).validate()
        if len(self.value) < 3:
            raise ValueError('Too short')


class UserProfile(jf.Obj):
    first_name = jf.Str(validators=[])
    last_name = LastName()

    def validate(self):
        super(UserProfile, self).validate()
        if not (self.first_name or self.last_name):
            raise ValueError('Requiered firstname or lastname')


def valid_user_ids(value):
    print('DDDDDDDDDDDDDD')
    print(value)
    if value not in [1, 2, 3]:
        raise ValueError('Value must be 1, 2 or 3')


def allow_city(*args):
    cities = args

    def inner(value):
        print('IIIIIIII')
        print(cities)
        print(value)
        if value not in cities:
            raise ValueError('This city is not allow')

    return inner


def valid_first_letter(letter):
    def inner(value):
        print('VFL')
        print(value)
        print(value.city)
        print(value.street)
        if value.city and value.street:
            if value.city[0] != value.street[0]:
                raise ValueError('First letter error')
    return inner


def valid_lenght(value):
    print('LLLLL')
    if len(value.city) > 5 or len(value.street) > 5:
        raise ValueError('Too long')


class Validators(jrlib.Method):
    user_id = jf.Int(validators=[valid_user_ids])
    age = jf.Int()
    gender = jf.Str()
    user_profile = UserProfile()
    address = jf.Obj(
        fields=dict(
            city=jf.Str(required=True,
                        validators=[allow_city('london', 'msk', 'ny')]),
            street=jf.Str()
        ),
        required=False,
        validators=[valid_first_letter('m'), valid_lenght]
    )

    def execute(self):
        print('up: {}'.format(self.user_profile))
        return {
            'user_id': self.user_id,
            'age': self.age,
            'user_profile': {
                'first_name': self.user_profile.first_name
            }
        }

    def validate(self):
        super(Validators, self).validate()
        if not (self.age or self.gender):
            raise ValueError('Requiered age or gender')

    def validate_gender(self, value):
        print('GGGGGGGGG')
        print(value)
        if len(value) > 1:
            raise ValueError('Too long')
