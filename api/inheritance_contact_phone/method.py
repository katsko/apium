from jrlib import jf
from api_base.contact.base_method import BaseContact


class InheritanceContactPhone(BaseContact):
    phone = jf.Str()

    def execute(self):
        return {
            "user_id": self.user_id,
            "comment": self.comment,
            "phone": self.phone,
        }

    def validate(self):
        super(InheritanceContactPhone, self).validate()
        if not self.phone or len(self.phone) != self.user_id:
            raise ValueError("Error phone lenght")
