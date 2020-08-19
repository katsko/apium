import jrlib
from jrlib import jf


class UserProfile(jf.Obj):
    first_name = jf.Str(required=True)
    # first_name = jf.Str()
    last_name = jf.Str()


class SetObjFieldRequired(jrlib.Method):
    user_id = jf.Int(required=True)
    # user_profile = UserProfile(required=True)
    user_profile = UserProfile()

    def execute(self):
        return {
            "user_id": self.user_id,
        }
