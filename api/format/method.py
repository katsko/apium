import jrlib
from jrlib import jf


class StripStr(jf.Str):
    def format(self):
        self.value = super(StripStr, self).format()
        if isinstance(self.value, str):
            return self.value.strip()
        return self.value


class UserProfile(jf.Obj):
    first_name = jf.Str()
    last_name = StripStr()

    def format(self):
        if "middle_name" in self.value and "first_name" in self.value:
            self.value["first_name"] = "{} {}".format(
                self.value["first_name"], self.value["middle_name"]
            )
        return self.value


class Format(jrlib.Method):
    user_id = jf.Int()
    age = jf.Float()
    gender = jf.Str()
    user_profile = UserProfile()

    def execute(self):
        return {
            "user_id": self.user_id,
            "age": self.age,
            "gender": self.gender,
            "user_profile": {
                "first_name": self.user_profile.first_name,
                "last_name": self.user_profile.last_name,
            },
        }
