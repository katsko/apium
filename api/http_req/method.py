import jrlib


class HttpReq(jrlib.Method):
    def execute(self):
        return {
            "user_agent": self.request.META.get("HTTP_USER_AGENT"),
            "url": self.request.build_absolute_uri(),
        }
