import jrlib
from jrlib import jf
from storage.data import USERS, CITIES


class AuthCheck(jrlib.Method):
    auth = jf.Obj(
        fields=dict(
            username=jf.Str(required=True, nullable=False),
            password=jf.Str(required=True, nullable=False),
        ),
        required=True,
        nullable=False,
        order=-100,
    )

    @jrlib.order(-100)
    def __middle(self):
        user = USERS.get(self.auth.username)
        if not user or (user and user.get("password") != self.auth.password):
            raise ValueError("Access denied")
        self.method_cache["auth_user"] = user


class CacheTestField(jf.Str):

    def validate(self):
        super(CacheTestField, self).validate()
        print("1 validator CacheTestField")
        print(self.method_cache)


class CacheTestObjField(jf.Obj):
    test_obj_inner = jf.Str(default=1)

    def validate(self):
        super(CacheTestObjField, self).validate()
        print("2 validator CacheTestObjField")
        print(self.method_cache)


class GetCache(AuthCheck):
    test = CacheTestField(default=1)
    test_obj = CacheTestObjField(default={"test_obj_inner": 1})

    def execute(self):
        print("3 execute GetCache")
        print(self.method_cache)
        user = self.method_cache["auth_user"]
        name = user.get("name")
        city_id = user.get("city_id")
        city = CITIES.get(city_id, {})
        return {
            "name": name,
            "city": city,
        }
