import unittest
from unittest.mock import patch, MagicMock
from wiki.web.forms import URLForm, SearchForm, EditorForm, LoginForm, CommentForm, LikeForm, AddToCartForm, ShoppingInfoForm, PurchasingForm, CreateForm, UserForm


class TestForms(unittest.TestCase):
    def test_url_form_validation(self):
        form_data = {'url': 'test-page'}
        with patch('wiki.web.user.current_wiki.exists', return_value=False) as mock_exists:
            form = URLForm(data=form_data)
            self.assertTrue(form.validate())
        mock_exists.assert_called_once_with('test-page')

        with patch('wiki.web.user.current_wiki.exists', return_value=True):
            form = URLForm(data=form_data)
            self.assertFalse(form.validate())

    def test_login_form_validation(self):
        form_data = {'name': 'user', 'password': 'pass'}
        user_mock = MagicMock()
        user_mock.check_password.return_value = True
        with patch('wiki.web.user.current_users.get_user', return_value=user_mock):
            form = LoginForm(data=form_data)
            self.assertTrue(form.validate())

        user_mock.check_password.return_value = False
        with patch('wiki.web.user.current_users.get_user', return_value=user_mock):
            form = LoginForm(data=form_data)
            self.assertFalse(form.validate())
            self.assertIn('Username and password do not match.', form.password.errors)

        with patch('wiki.web.user.current_users.get_user', return_value=None):
            form = LoginForm(data=form_data)
            self.assertFalse(form.validate())
            self.assertIn('This username does not exist.', form.name.errors)

    def test_editor_form_validation(self):
        form_data = {'title': 'New Article', 'body': 'Some content'}
        form = EditorForm(data=form_data)
        self.assertTrue(form.validate())

    def test_create_form_validation(self):
        form_data = {'name': 'newuser', 'password': 'newpassword'}
        with patch('wiki.web.user.current_users.get_user', return_value=None):
            form = CreateForm(data=form_data)
            self.assertTrue(form.validate())

        with patch('wiki.web.user.current_users.get_user', return_value=True):
            form = CreateForm(data=form_data)
            self.assertFalse(form.validate())
            self.assertIn('This username already exists.', form.name.errors)

if __name__ == '__main__':
    unittest.main()
