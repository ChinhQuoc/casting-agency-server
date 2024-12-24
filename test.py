import os
import unittest
import json
from app import app
from app.models import setup_db, Movie, Actor, db

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = app.test_client

        # Configure the database for testing
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{}:{}@{}/{}'.format(
            os.environ.get('DB_USER'),
            os.environ.get('DB_PASSWORD'),
            'localhost:5432',
            os.environ.get('DB_NAME')
        )
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        with app.app_context():
            db.create_all()

        # Tokens for RBAC testing
        self.casting_assistant_token = os.environ.get('TOKEN_TEST')
        self.casting_director_token = 'CASTING_DIRECTOR_TOKEN'
        self.executive_producer_token = 'EXECUTIVE_PRODUCER_TOKEN'

        self.new_movie = {
            "title": "Test Movie",
            "releaseDate": "2024-01-01",
            "idsActor": []
        }

        self.new_actor = {
            "name": "Test Actor",
            "age": 30,
            "gender": "male",
            "idsMovie": []
        }

    def tearDown(self):
        """Executed after each test"""
        pass

    def get_headers(self, token):
        return {
            "Authorization": f"Bearer {token}"
        }

    def test_get_movies_success(self):
        res = self.client().get('/movies', headers=self.get_headers(self.casting_assistant_token))
        print('res: ', res)
        self.assertEqual(res.status_code, 200)

        try:
            data = json.loads(res.data)
        except json.JSONDecodeError:
            self.fail("Response is not valid JSON")

        self.assertTrue(data['success'])
        self.assertIsInstance(data['movies'], list)

    # def test_get_movies_unauthorized(self):
    #     res = self.client().get('/movies')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data['success'])

    # def test_post_movie_success(self):
    #     res = self.client().post('/movies', headers=self.get_headers(self.executive_producer_token), json=self.new_movie)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertIsInstance(data['movie'], dict)

    # def test_post_movie_unauthorized(self):
    #     res = self.client().post('/movies', headers=self.get_headers(self.casting_assistant_token), json=self.new_movie)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # Success and error tests for actors
    # def test_get_actors_success(self):
    #     res = self.client().get('/actors', headers=self.get_headers(self.casting_assistant_token))
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertIsInstance(data['actors'], list)

    # def test_get_actors_unauthorized(self):
    #     res = self.client().get('/actors')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data['success'])

    # def test_post_actor_success(self):
    #     res = self.client().post('/actors', headers=self.get_headers(self.casting_director_token), json=self.new_actor)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertIsInstance(data['actor'], dict)

    # def test_post_actor_unauthorized(self):
    #     res = self.client().post('/actors', headers=self.get_headers(self.casting_assistant_token), json=self.new_actor)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 403)
    #     self.assertFalse(data['success'])

    # # RBAC tests
    # def test_casting_assistant_access(self):
    #     res = self.client().get('/movies', headers=self.get_headers(self.casting_assistant_token))
    #     self.assertEqual(res.status_code, 200)

    #     res = self.client().post('/movies', headers=self.get_headers(self.casting_assistant_token), json=self.new_movie)
    #     self.assertEqual(res.status_code, 403)

    # def test_casting_director_access(self):
    #     res = self.client().post('/actors', headers=self.get_headers(self.casting_director_token), json=self.new_actor)
    #     self.assertEqual(res.status_code, 200)

    #     res = self.client().delete('/movies/1', headers=self.get_headers(self.casting_director_token))
    #     self.assertEqual(res.status_code, 403)

    # def test_executive_producer_access(self):
    #     res = self.client().post('/movies', headers=self.get_headers(self.executive_producer_token), json=self.new_movie)
    #     self.assertEqual(res.status_code, 200)

    #     res = self.client().delete('/movies/1', headers=self.get_headers(self.executive_producer_token))
    #     self.assertEqual(res.status_code, 200)


# Run tests
if __name__ == "__main__":
    unittest.main()