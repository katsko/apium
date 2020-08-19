import jrlib
from jrlib import jf


class SetAnyType(jrlib.Method):
    user_id = jf.Int(required=True)
    any_data = jf.Field()

    def execute(self):
        return {
            "user_id": str(type(self.user_id)),
            "any_data": str(type(self.any_data)),
        }
