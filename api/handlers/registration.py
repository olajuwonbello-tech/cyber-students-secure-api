# I handle new user registration and securely store user credentials and personal data

from tornado.escape import json_decode

from .base import BaseHandler
from api.security_utils import hash_password, encrypt_value


class RegistrationHandler(BaseHandler):

    async def post(self):
        try:
            body = json_decode(self.request.body)

            # I normalize email input to avoid duplicates
            email = body['email'].lower().strip()
            password = body['password']

            display_name = body.get('displayName')
            if display_name is None:
                display_name = email

            if not isinstance(display_name, str):
                raise Exception()

            # I collect additional sensitive user data
            full_name = body.get('fullName', '')
            phone = body.get('phone', '')
            address = body.get('address', '')
            dob = body.get('dob', '')
            disability = body.get('disability', '')

        except Exception:
            self.send_error(400, message='You must provide an email address, password and display name!')
            return

        # I validate required fields
        if not email:
            self.send_error(400, message='The email address is invalid!')
            return

        if not password:
            self.send_error(400, message='The password is invalid!')
            return

        if not display_name:
            self.send_error(400, message='The display name is invalid!')
            return

        # I check for duplicate users
        user = await self.db.users.find_one({'email': email})

        if user is not None:
            self.send_error(409, message='A user with the given email address already exists!')
            return

        # I securely hash the password before storing it
        password_data = hash_password(password)

        # I encrypt sensitive personal fields before saving them
        await self.db.users.insert_one({
            'email': email,
            'passwordHash': password_data['passwordHash'],
            'passwordSalt': password_data['passwordSalt'],
            'passwordIterations': password_data['passwordIterations'],
            'displayName': display_name,
            'fullName': encrypt_value(full_name),
            'phone': encrypt_value(phone),
            'address': encrypt_value(address),
            'dob': encrypt_value(dob),
            'disability': encrypt_value(disability),
        })

        self.set_status(200)
        self.response['email'] = email
        self.response['displayName'] = display_name

        self.write_json()