from tornado.escape import json_decode
from tornado.httputil import HTTPHeaders
from tornado.ioloop import IOLoop
from tornado.web import Application

from api.handlers.user import UserHandler
from api.security_utils import hash_password, hash_token, encrypt_value

from .base import BaseTest


class UserHandlerTest(BaseTest):

    @classmethod
    def setUpClass(self):
        self.my_app = Application([(r'/user', UserHandler)])
        super().setUpClass()

    async def register(self):
        password_data = hash_password(self.password)
        await self.get_app().db.users.insert_one({
            'email': self.email,
            'passwordHash': password_data['passwordHash'],
            'passwordSalt': password_data['passwordSalt'],
            'passwordIterations': password_data['passwordIterations'],
            'displayName': self.display_name,
            'fullName': encrypt_value(self.full_name),
            'phone': encrypt_value(self.phone),
            'address': encrypt_value(self.address),
            'dob': encrypt_value(self.dob),
            'disability': encrypt_value(self.disability),
        })

    async def login(self):
        await self.get_app().db.users.update_one({
            'email': self.email
        }, {
            '$set': {
                'tokenHash': hash_token(self.token),
                'expiresIn': 2147483647
            }
        })

    def setUp(self):
        super().setUp()

        self.email = 'test@test.com'
        self.password = 'testPassword'
        self.display_name = 'testDisplayName'
        self.token = 'testToken'

        self.full_name = 'John Doe'
        self.phone = '123456789'
        self.address = 'Street 1'
        self.dob = '2000-01-01'
        self.disability = 'None'

        IOLoop.current().run_sync(self.register)
        IOLoop.current().run_sync(self.login)

    def test_user(self):
        headers = HTTPHeaders({'X-Token': self.token})

        response = self.fetch('/user', headers=headers)
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(self.email, body_2['email'])
        self.assertEqual(self.display_name, body_2['displayName'])

    def test_user_returns_decrypted_personal_data(self):
        headers = HTTPHeaders({'X-Token': self.token})

        response = self.fetch('/user', headers=headers)
        self.assertEqual(200, response.code)

        body_2 = json_decode(response.body)
        self.assertEqual(self.full_name, body_2['fullName'])
        self.assertEqual(self.phone, body_2['phone'])
        self.assertEqual(self.address, body_2['address'])
        self.assertEqual(self.dob, body_2['dob'])
        self.assertEqual(self.disability, body_2['disability'])

    def test_personal_data_is_stored_encrypted(self):
        user = IOLoop.current().run_sync(
            lambda: self.get_app().db.users.find_one({'email': self.email})
        )

        self.assertIsInstance(user['fullName'], dict)
        self.assertIsInstance(user['phone'], dict)
        self.assertIsInstance(user['address'], dict)
        self.assertIsInstance(user['dob'], dict)
        self.assertIsInstance(user['disability'], dict)

        self.assertIn('ciphertext', user['fullName'])
        self.assertIn('nonce', user['fullName'])
        self.assertIn('ciphertext', user['phone'])
        self.assertIn('nonce', user['phone'])

        self.assertNotEqual(self.full_name, user['fullName']['ciphertext'])
        self.assertNotEqual(self.phone, user['phone']['ciphertext'])
        self.assertNotEqual(self.address, user['address']['ciphertext'])
        self.assertNotEqual(self.dob, user['dob']['ciphertext'])
        self.assertNotEqual(self.disability, user['disability']['ciphertext'])

    def test_user_without_token(self):
        response = self.fetch('/user')
        self.assertEqual(400, response.code)

    def test_user_wrong_token(self):
        headers = HTTPHeaders({'X-Token': 'wrongToken'})

        response = self.fetch('/user', headers=headers)
        self.assertEqual(403, response.code)