from tornado.web import authenticated

from .auth import AuthHandler
from api.security_utils import decrypt_value


class UserHandler(AuthHandler):

    @authenticated
    async def get(self):
        user = await self.db.users.find_one({
            'email': self.current_user['email']
        })

        self.set_status(200)
        self.response['email'] = user['email']
        self.response['displayName'] = user['displayName']
        self.response['fullName'] = decrypt_value(user.get('fullName'))
        self.response['phone'] = decrypt_value(user.get('phone'))
        self.response['address'] = decrypt_value(user.get('address'))
        self.response['dob'] = decrypt_value(user.get('dob'))
        self.response['disability'] = decrypt_value(user.get('disability'))

        self.write_json()