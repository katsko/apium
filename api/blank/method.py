import jrlib
from jrlib import jf


class Pr_2(jf.Obj):
    p_f1 = jf.Str()
    p_f2 = jf.Str(blank=False)


class Blank(jrlib.Method):
    name = jf.Str()
    gender = jf.Str(required=True, blank=False)
    email = jf.Email(blank=False)
    data = jf.Dict(blank=False)
    cities = jf.List(blank=False)
    profile_1 = jf.Obj(fields=dict(f1=jf.Str()), blank=False)
    profile_2 = Pr_2(blank=False)

    def execute(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "email": self.email,
        }
