from app.api.base import BaseHandler


class HelloHandler(BaseHandler):
    def get(self):
        data = 'hello word'
        return self.response_format(data=data)
