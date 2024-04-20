import json
import os
import unittest
from unittest import TestCase, mock
from wiki.web.user import UserManager, User, make_salted_hash, check_hashed_password

class TestUserManager(TestCase):
    def setUp(self):
        self.mock_path = '/fakepath'
        self.manager = UserManager(self.mock_path)

    @mock.patch('os.path.exists')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='{}')
    def test_read_no_existing_file(self, mock_open, mock_exists):
        mock_exists.return_value = False
        result = self.manager.read()
        self.assertEqual(result, {})

    @mock.patch('os.path.exists')
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_read_existing_file(self, mock_open, mock_exists):
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps({'testuser': 'testdata'})
        result = self.manager.read()
        self.assertEqual(result, {'testuser': 'testdata'})

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_write(self, mock_open):
        test_data = {'testuser': 'testdata'}
        self.manager.write(test_data)
        mock_open.assert_called_once_with(os.path.join(self.mock_path, 'users.json'), 'w')
        handle = mock_open()
        handle.write.assert_called_once_with(json.dumps(test_data, indent=2))

    @mock.patch('wiki.web.user.UserManager.read')
    def test_get_user(self, mock_read):
        mock_read.return_value = {'existinguser': {'user_id': 1}}
        user = self.manager.get_user('existinguser')
        self.assertIsInstance(user, User)
        self.assertEqual(user.name, 'existinguser')

    @mock.patch('wiki.web.user.UserManager.read')
    @mock.patch('wiki.web.user.UserManager.write')
    def test_delete_user(self, mock_write, mock_read):
        mock_read.return_value = {'testuser': {}}
        result = self.manager.delete_user('testuser')
        self.assertFalse(result)

class TestUser(TestCase):
    def setUp(self):
        self.manager = mock.MagicMock()
        self.user_data = {
            'name': 'testuser',
            'authentication_method': 'cleartext',
            'password': 'password123',
            'active': True,
            'authenticated': False
        }
        self.user = User(self.manager, 'testuser', self.user_data)

    def test_check_password_cleartext(self):
        result = self.user.check_password('password123')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
