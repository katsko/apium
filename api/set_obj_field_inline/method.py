import jrlib
from jrlib import jf


class UserProfile(jf.Obj):
    first_name = jf.Str()
    last_name = jf.Str()
    test = "abc test"


class SetObjFieldInline(jrlib.Method):
    user_id = jf.Int(required=True)
    user_profile = UserProfile()
    address = jf.Obj(
        fields=dict(city=jf.Str(required=True), street=jf.Str()),
        required=False,
    )

    def execute(self):
        print("sss")
        print(self.user_profile.first_name)
        print(self.user_profile.last_name)
        print("eee")
        return {
            "user_id": self.user_id,
            "user_profile": {
                "first_name": self.user_profile.first_name,
                "last_name": self.user_profile.last_name,
                "city": self.address.city,
                "street": self.address.street,
            },
        }
