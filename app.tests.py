import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFUSkJORE5ETWtWQ09UTkJOVUpCUlRBd05VRTVRVGd4TmpjMU5FUTJOekF5T1RWRU5qRkVOUSJ9.eyJpc3MiOiJodHRwczovL3VraHUtbW92aWUtY2FzdC1hcGkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2M4YjEwMDY0ZTM0MGY4NTM3YzFjMCIsImF1ZCI6Im1vdmllLWNhc3QiLCJpYXQiOjE1ODEwNzcwMjIsImV4cCI6MTU4MTA4NDIyMiwiYXpwIjoiNGd6WmJJd3FTbTJtaEJ5WGhWTFowejJUNXRSaFZwSUMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsIm1vZGlmeTphY3RvciIsIm1vZGlmeTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.E6qvwuAsOlRWlSxsSjMIcpZq49Jv8tB37NDQu5sYnIBk4T_Sv7F1iJ_FKEnMz-5DjkwMyNL3Dl0B7YDYqUma-AkYnto3Are2hH9pwHfaxvNIEjw3icRVAYyWbKTwcO4cVELmmr_PiHzHD1aJ-71T9RrhhMEfj2I5yjA6jXnrjLLlEV1QQSlb8zDlztPZYGOi7TYMGy3v-F-i_gaDYEIM8xkVcAkbBVuQdxU782Ezbxj_9Q2sNyEozQBZXBTzH4GQBFvZ3a3GxgI3ZV6yz_pQWi4uRvHVtTgVocajOTR9spdYocFGUckQLxwxAQYtoGfLFzMa1HL98cAkahaINwP0Rw'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFUSkJORE5ETWtWQ09UTkJOVUpCUlRBd05VRTVRVGd4TmpjMU5FUTJOekF5T1RWRU5qRkVOUSJ9.eyJpc3MiOiJodHRwczovL3VraHUtbW92aWUtY2FzdC1hcGkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2M4OTM0MTEwNGFjMGVhMDUxOTQ3NSIsImF1ZCI6Im1vdmllLWNhc3QiLCJpYXQiOjE1ODEwNzcwNjUsImV4cCI6MTU4MTA4NDI2NSwiYXpwIjoiNGd6WmJJd3FTbTJtaEJ5WGhWTFowejJUNXRSaFZwSUMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsIm1vZGlmeTphY3RvciIsIm1vZGlmeTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.bCwinYJNyJTuBKEh6yHzWJ9KJgkgPCq9TUi8AkgIpjdxJK1HEUvteINpQU6eS2JTcCKwhhhSbCTfa3ZNpehxKrnxS4NBDxidGm3atPf-CdlgJzM1LpvP8dIoB_i-sgj1sKaNULPNvwTpObhswSxxT77SMyuRcqbij76BA_xT7ZDrKIpxu_cnKQsFbVoZ5miJUkn8qW8JssiPWU9JaibYzp89FaHwg3Y7ghf1p58UNWbMrn8t5kgmTcCeZ1EAY9g00gWtV5pIWLtRNemmftUnEX60RZcfcEE5pxbwGHQOwoYtH9HxhDHPNJ3Sh1XkVeLWhdXXdam0r3RFqbArPkvHRw'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFUSkJORE5ETWtWQ09UTkJOVUpCUlRBd05VRTVRVGd4TmpjMU5FUTJOekF5T1RWRU5qRkVOUSJ9.eyJpc3MiOiJodHRwczovL3VraHUtbW92aWUtY2FzdC1hcGkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2M4Yjk3MzNmZGYzMGU5YWNjY2Y2YyIsImF1ZCI6Im1vdmllLWNhc3QiLCJpYXQiOjE1ODEwNzcxMDYsImV4cCI6MTU4MTA4NDMwNiwiYXpwIjoiNGd6WmJJd3FTbTJtaEJ5WGhWTFowejJUNXRSaFZwSUMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.Xh5sncplsXbcUUuS0snKED0Uxy-99Q1J-W72YF9IYq3MFOCLFCrbQa-A2NxA9LNhTWWuEaQ8ZfLF0xUZL8Gdf1G0S8fZ23iyoBZBe7HCdQBSs9pKQVhFJuTIqIdmPkt_ky038K7NJZdZWYmg8iImXVk2d4PQD32dyaj0tuVZ3uuLxn5RQ4CrVGFr_bEjzAHwf8MdfZwyHnFhJZaUje-_bGdM7bBi2HxqkQNV2v6tG9bZ9yeeH_R4gnq2dUkDblNksv7Y77X3gV5GAQ2SO-e6SHlaHN97J9iJyIlWQ-bXCrV9gaiZLQlvHAHTWJ5JsZON06QZEyWlMMizbRI3mUR2Og'

unittest.TestLoader.sortTestMethodsUsing = None

class MovieCastTestCase(unittest.TestCase):
    '''
    This class represent the test case for the Movie Cast API
    '''

    def setUp(self):

        '''
        Define test variables and initialize app.
        '''

        self.app = create_app()
        self.client = self.app.test_client

        self.new_actor = {
            'name': 'Matt Gunston',
            'age': 37,
            'gender': 'male'
        }
        self.invalid_actor = {
            'name': 'Chun Leyla',
            'gender': 'female'
        }
        self.new_movie = {
            'title': 'La La Land',
            'release_date': '11-11-2020',
        }
        self.invalid_movie = {
            'title': 'The Jigsaw Man',
        }

        setup_db(self.app)

    def tearDown(self):
        '''
        Executed after reach test
        '''
        pass


    '''
    POST /actors
    '''
    def test_1a_add_actor_success_201(self):
        print('ADD ACTOR')
        response = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully added actor')
        self.assertEqual(data['actor']['name'], 'Matt Gunston')

    def test_1b_add_actor_failure_400(self):
        response = self.client().post(
            '/actors',
            json=self.invalid_movie,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # RABC - Casting Assistant
    def test_1c_add_actor_failure_403_casting_assistant(self):
        response = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Access denied. Permission not found')

    
    '''
    POST /movies
    '''
    def test_2a_add_movie_success_201(self):
        print('ADD MOVIE')
        response = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully added movie')
        self.assertEqual(data['movie']['title'], 'La La Land')

    def test_2b_add_movie_failure_400(self):
        response = self.client().post(
            '/movies',
            json=self.invalid_movie,
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # RABC - Casting Director
    def test_2c_add_movie_failure_403_casting_director(self):
        response = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Access denied. Permission not found')


    '''
    Get /actors
    '''
    def test_3a_get_all_actors_success_200(self):
        print('GET ACTOR')
        response = self.client().get(
            '/actors',
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully returned all actors')
        self.assertTrue(data['actors'])

    def test_3b_get_all_actors_failure_401(self):
        response = self.client().get(
            '/movies',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])

    '''
    Get /movies
    '''
    def test_4a_get_all_movies_success_200(self):
        print('GET MOVIE')
        response = self.client().get(
            '/movies',
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully returned all movies')
        self.assertTrue(data['movies'])

    def test_4b_get_all_movies_failure_401(self):
        response = self.client().get(
            '/movies',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])


    '''
    PATCH /actor/<int:id>
    '''
    def test_5a_update_actor_success_200(self):
        print('UPDATE ACTOR')
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Matt Ginsberg'},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully updated actor details')
        self.assertEqual(data['actor']['name'], 'Matt Ginsberg')

    def test_5b_update_actor_failure_400(self):
        response = self.client().patch(
            '/actors/1',
            json={},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    '''
    PATCH /movie/<int:id>
    '''
    def test_6a_update_movie_success_200(self):
        print('UPDATE MOVIE')
        response = self.client().patch(
            '/movies/1',
            json={'title': 'The La La Land'},
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully updated movie details')
        self.assertEqual(data['movie']['title'], 'The La La Land')

    def test_6b_update_movie_failure_404(self):
        response = self.client().patch(
            '/movies/10',
            json={'title': 'The La La Land'},
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    # RABC - Casting Assistant
    def test_6c_update_movie_failure_403_casting_assistant(self):
        response = self.client().patch(
            '/movies/1',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Access denied. Permission not found')


    '''
    DELETE /actors/<int:id>
    '''
    def test_7a_delete_actor_success(self):
        print('DELETE ACTOR')
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully deleted actor')
        self.assertEqual(data['deleted_id'], 1)

    def test_7b_delete_actor_failure_404(self):
        response = self.client().delete(
            '/actors/10',
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    
    '''
    DELETE /movies/<int:id>
    '''
    def test_8a_delete_movie_success(self):
        print('DELETE MOVIE')
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully deleted movie')
        self.assertEqual(data['deleted_id'], 1)

    def test_8b_delete_movie_failure_404(self):
        response = self.client().delete(
            '/movies/10',
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    # RABC - Casting Director
    def test_8c_delete_movie_failure_403_casting_director(self):
        response = self.client().delete(
            '/movies/10',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(data['message'], 'Access denied. Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
