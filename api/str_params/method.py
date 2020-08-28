import jrlib
from jrlib import jf


class StrParams(jrlib.Method):
    country = jf.Str()
    city = jf.Str(strip=False)
    street = jf.Str(min_lenght=2, max_lenght=10)
    house = jf.Str(cut=3)

    def execute(self):
        return {
            "country": self.country,
            "city": self.city,
            "street": self.street,
            "house": self.house,
        }
