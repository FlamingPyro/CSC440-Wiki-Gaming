import unittest
from sqlite3 import IntegrityError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from sqlalchemy.testing import db
from wiki.web.models import Destiny, LethalCompany, Minecraft, Tekken, EldenRing, Palworld, HorizonForbiddenWest, Helldivers, ShoppingInfo, HomeDatabase


class BaseTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(BaseTestCase):
    def test_destiny_model(self):
        # Create an instance of the Destiny model
        destiny = Destiny(username='player1', comments='Great game!', numLikes=10)
        db.session.add(destiny)
        db.session.commit()

        # Retrieve the instance back
        retrieved = Destiny.query.first()
        self.assertEqual(retrieved.username, 'player1')
        self.assertEqual(retrieved.comments, 'Great game!')
        self.assertEqual(retrieved.numLikes, 10)

    def test_lethal_company_defaults(self):
        # Test default values
        lethal = LethalCompany(username='player2', comments='Challenging missions')
        db.session.add(lethal)
        db.session.commit()

        retrieved = LethalCompany.query.first()
        self.assertEqual(retrieved.numLikes, 0)  # Default value check

    def test_shopping_info_constraints(self):
        # Ensure nullable constraints are respected
        shopping = ShoppingInfo(name='John Doe', address='123 Elm St', city='Springfield', state='IL',
                                country='USA', zipcode='62704', email='johndoe@example.com', phone_number='555-1234')
        db.session.add(shopping)
        db.session.commit()

        retrieved = ShoppingInfo.query.first()
        self.assertEqual(retrieved.email, 'johndoe@example.com')

    def test_home_database_not_nullable(self):
        # Test not nullable fields
        home = HomeDatabase(name='Elegant Home', icon='icon.png', price='350000')
        db.session.add(home)
        try:
            db.session.commit()
        except Exception as e:
            self.assertTrue(isinstance(e, IntegrityError))

if __name__ == '__main__':
    unittest.main()
