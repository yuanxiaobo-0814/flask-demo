from app.api.base import BaseHandler
from app.models.user import User


class UserHandler(BaseHandler):
    def get(self):
        data = {
            'name': 'yuan',
            'age': 25,
            'phone': '18666291456'
        }
        return self.response_format(data=data)
