import jrlib
from jrlib import jf
from storage.data import USERS, CITIES


class AuthCheck(jrlib.Method):
    def __middle(self):
        is_auth = self.request.COOKIES.get("is_auth") == "True"
        if not is_auth:
            raise ValueError("Access denied")


class IdField(jf.Str):
    def __init__(self, dataset, *args, **kwargs):
        super(IdField, self).__init__(*args, **kwargs)
        self.required = True
        self.nullable = False
        self.dataset = dataset

    def validate(self):
        super(IdField, self).validate()
        if self.value not in self.dataset:
            raise ValueError("id not found")


class GetUserProfile(AuthCheck):
    user_id = IdField(dataset=USERS)

    def execute(self):
        user = USERS[self.user_id]
        name = user.get("name")
        city_id = user.get("city_id")
        city = CITIES.get(city_id, {})
        return {
            "name": name,
            "city": city,
        }
