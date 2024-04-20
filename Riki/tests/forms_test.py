import unittest
from flask import Flask
from flask_testing import TestCase
from wiki.web.forms import CommentForm, LikeForm, AddToCartForm, ShoppingInfoForm, PurchasingForm


class BaseTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app


class TestCommentForm(BaseTestCase):
    def test_comment_required(self):
        form = CommentForm(comment="")
        self.assertFalse(form.validate())

    def test_valid_comment(self):
        form = CommentForm(comment="Nice article!")
        self.assertTrue(form.validate())


class TestShoppingInfoForm(BaseTestCase):
    def test_valid_input(self):
        form = ShoppingInfoForm(data={
            'name': 'John Doe',
            'address': '123 Main St',
            'city': 'Anytown',
            'state': 'Anystate',
            'country': 'US',
            'zipcode': '12345',
            'email': 'john@example.com',
            'phone_number': '1234567890'
        })
        self.assertTrue(form.validate())

    def test_invalid_input(self):
        form = ShoppingInfoForm(data={
            'name': '',
            'address': '',
            'city': '',
            'state': '',
            'country': '',
            'zipcode': '',
            'email': '',
            'phone_number': ''
        })
        self.assertFalse(form.validate())
        self.assertTrue(all(field in form.errors for field in ['name', 'address', 'city', 'state', 'country', 'zipcode', 'email', 'phone_number']))


class TestPurchasingForm(BaseTestCase):
    def test_valid_credit_card_info(self):
        form = PurchasingForm(data={
            'credit_card_number': '4111111111111111',
            'card_holder': 'John Doe',
            'card_expiration_date': '12/24',
            'card_cvv': '123'
        })
        self.assertTrue(form.validate())

    def test_invalid_credit_card_info(self):
        form = PurchasingForm(data={
            'credit_card_number': '',
            'card_holder': '',
            'card_expiration_date': '',
            'card_cvv': ''
        })
        self.assertFalse(form.validate())
        self.assertTrue(all(field in form.errors for field in ['credit_card_number', 'card_holder', 'card_expiration_date', 'card_cvv']))


if __name__ == '__main__':
    unittest.main()
