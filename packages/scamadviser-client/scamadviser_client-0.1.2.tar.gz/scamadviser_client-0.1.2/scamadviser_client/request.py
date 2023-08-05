import requests


class Request:
    def __init__(self, method: str, path: str):
        self.method = method.upper()
        self.h = {"Content-Type": "application/json;charset=UTF-8"}
        self.path = path

    def __call__(self, f):
        def wrapper(obj, *args, **kwargs):
            payload = f(obj, *args, **kwargs)
            args = {
                "method": self.method,
                "url": "https://{}/{}".format(obj.host, self.path),
                "headers": self.h,
            }
            if payload is not None:
                args["json"] = payload
            return requests.request(**args)

        return wrapper
