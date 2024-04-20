import unittest
from wiki.web.extensions import db
from wiki.web.models import Destiny, LethalCompany, ShoppingInfo, HomeDatabase
from flask import Flask

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        with app.app_context():
            db.create_all()
        self.app = app

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_destiny_model(self):
        with self.app.app_context():
            model_instance = Destiny(username='testuser', comments='A sample comment', numLikes=15)
            db.session.add(model_instance)
            db.session.commit()
            queried_instance = Destiny.query.first()
            self.assertEqual(queried_instance.username, 'testuser')
            self.assertEqual(queried_instance.comments, 'A sample comment')
            self.assertEqual(queried_instance.numLikes, 15)

    def test_lethal_company_model(self):
        with self.app.app_context():
            model_instance = LethalCompany(username='user123', comments='Another comment', numLikes=20)
            db.session.add(model_instance)
            db.session.commit()
            queried_instance = LethalCompany.query.first()
            self.assertEqual(queried_instance.username, 'user123')
            self.assertEqual(queried_instance.comments, 'Another comment')
            self.assertEqual(queried_instance.numLikes, 20)

    def test_shopping_info_model(self):
        with self.app.app_context():
            model_instance = ShoppingInfo(
                name='Store A', address='123 Market St', city='Anytown',
                state='Anystate', country='Anycountry', zipcode='12345',
                email='contact@storea.com', phone_number='123-456-7890'
            )
            db.session.add(model_instance)
            db.session.commit()
            queried_instance = ShoppingInfo.query.first()
            self.assertEqual(queried_instance.name, 'Store A')
            self.assertEqual(queried_instance.address, '123 Market St')
            self.assertEqual(queried_instance.city, 'Anytown')
            self.assertEqual(queried_instance.email, 'contact@storea.com')
            self.assertEqual(queried_instance.phone_number, '123-456-7890')

    def test_home_database_model(self):
        with self.app.app_context():
            model_instance = HomeDatabase(name='Lamp', icon='icon.png', price='9.99')
            db.session.add(model_instance)
            db.session.commit()
            queried_instance = HomeDatabase.query.first()
            self.assertEqual(queried_instance.name, 'Lamp')
            self.assertEqual(queried_instance.icon, 'icon.png')
            self.assertEqual(queried_instance.price, '9.99')

if __name__ == '__main__':
    unittest.main()
