import jrlib
from jrlib import jf


class LastName(jf.Str):
    def validate(self):
        super(LastName, self).validate()
        if len(self.value) < 3:
            raise ValueError("Too short")


class UserProfile(jf.Obj):
    first_name = jf.Str(default=None)
    last_name = LastName(default="l n")
    middle_name = jf.Str()

    # TODO: support this way for get default value
    def default_middle_name(self):
        print("MMMMMk")
        return "mid mid"


def get_house():
    print("HHHHH")
    return "hhhhhhh"


def get_address():
    print("AAAAA")
    return {"city": "cccc"}


class SetDefault(jrlib.Method):
    user_id = jf.Int()
    age = jf.Int(required=True)
    gender = jf.Str(default="g")
    user_profile = UserProfile()
    address = jf.Obj(
        fields=dict(
            city=jf.Str(required=True),
            street=jf.Str(default="ul"),
            house=jf.Str(default=get_house),
        ),
        default=get_address,
    )

    # TODO: support this way for get default value
    def default_user_id(self):
        print("UUUUU")
        return 100

    def execute(self):
        return {
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender,
            "user_profile": {
                "first_name": self.user_profile.first_name,
                "last_name": self.user_profile.last_name,
                "middle_name": self.user_profile.middle_name,
            },
            "address": {
                "city": self.address.city,
                "street": self.address.street,
                "house": self.address.house,
            },
        }
