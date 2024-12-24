# import os
# import unittest
# import json
# from app import app
# from app.models import setup_db, Movie, Actor, db

# class CastingAgencyTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = app
#         self.client = app.test_client

#         # Configure the database for testing
#         app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{}:{}@{}/{}'.format(
#             os.environ.get('DB_USER'),
#             os.environ.get('DB_PASSWORD'),
#             'localhost:5432',
#             os.environ.get('DB_NAME')
#         )
#         app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#         with app.app_context():
#             db.create_all()

#         # Tokens for RBAC testing
#         self.casting_assistant_token = os.environ.get('TOKEN_TEST')
#         self.casting_director_token = 'CASTING_DIRECTOR_TOKEN'
#         self.executive_producer_token = 'EXECUTIVE_PRODUCER_TOKEN'

#         self.new_movie = {
#             "title": "Test Movie",
#             "releaseDate": "2024-01-01",
#             "idsActor": []
#         }

#         self.new_actor = {
#             "name": "Test Actor",
#             "age": 30,
#             "gender": "male",
#             "idsMovie": []
#         }

#     def tearDown(self):
#         """Executed after each test"""
#         pass

#     def get_headers(self, token):
#         return {
#             "Authorization": f"Bearer {token}"
#         }
    
# # Run tests
# if __name__ == "__main__":
#     unittest.main()