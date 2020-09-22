import jrlib
from jrlib import jf


class SubUserProfile(jf.Obj):
    age = jf.Int()


class UserProfile(jf.Obj):
    first_name = jf.Str()
    sub = SubUserProfile()


class UseUndef(jrlib.Method):
    user_id = jf.Int()
    user_profile = UserProfile()

    def execute(self):
        print("execute")
        print("user_id")
        print(self.user_id)
        print("user_profile")
        print(self.user_profile)
        print("user_profile.first_name")
        print(self.user_profile.first_name)
        print("user_profile.sub")
        print(self.user_profile.sub)
        print("user_profile.sub.age")
        print(self.user_profile.sub.age)
        print("/execute")
        return {
            "user_id": self.user_id,
            "first_name": self.user_profile.first_name,
        }
