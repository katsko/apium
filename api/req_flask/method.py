import jrlib
from time import time
from jrlib import jf


class ReqFlask(jrlib.Method):
    msg = jf.Str(required=True)

    def execute(self):
        self.response.set_cookie("time", value="{}".format(int(time())))
        url = self.request.url
        user_agent = self.request.headers.get("User-Agent")
        return {
            "msg": self.msg,
            "url": url,
            "user_agent": user_agent,
        }
