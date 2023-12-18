import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, parent_dir)

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import RecModel, Base  # Replace 'your_module' with the actual module name where RecModel is

class TestRecModel(unittest.TestCase):
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.session = self.SessionLocal()

    def tearDown(self):
        # Drop all tables and close the session
        Base.metadata.drop_all(self.engine)
        self.session.close()

    def test_rec_model_creation(self):
        # Create an instance of the RecModel
        new_rec = RecModel(
            id=1,
            name='Test Rec',
            image_url='http://example.com/rec.png',
            landing_url='http://example.com',
            weight=10,
            target_country='US',
            target_gender='M',
            point=2.50
        )

        self.session.add(new_rec)
        self.session.commit()

        # Retrieve the instance to make sure it was correctly added to the database
        retrieved_rec = self.session.query(RecModel).filter_by(name='Test Rec').first()

        # Assertions to ensure that the object was correctly created and saved
        self.assertIsNotNone(retrieved_rec)
        self.assertEqual(retrieved_rec.id, 1)
        self.assertEqual(retrieved_rec.name, 'Test Rec')
        self.assertEqual(retrieved_rec.image_url, 'http://example.com/rec.png')
        self.assertEqual(retrieved_rec.landing_url, 'http://example.com')
        self.assertEqual(retrieved_rec.weight, 10)
        self.assertEqual(retrieved_rec.target_country, 'US')
        self.assertEqual(retrieved_rec.target_gender, 'M')
        self.assertEqual(retrieved_rec.point, 2.50)

if __name__ == '__main__':
    unittest.main()
