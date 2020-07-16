from jrlib import jf
from api_base.contact.base_method import BaseContact


class InheritanceContactEmail(BaseContact):
    email = jf.Email()

    def execute(self):
        return {
            'user_id': self.user_id,
            'comment': self.comment,
            'email': self.email,
        }

    def validate(self):
        super(InheritanceContactEmail, self).validate()
        if not self.email or len(self.email) != self.user_id:
            raise ValueError('Error email lenght')
