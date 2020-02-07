import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFUSkJORE5ETWtWQ09UTkJOVUpCUlRBd05VRTVRVGd4TmpjMU5FUTJOekF5T1RWRU5qRkVOUSJ9.eyJpc3MiOiJodHRwczovL3VraHUtbW92aWUtY2FzdC1hcGkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2M4YjEwMDY0ZTM0MGY4NTM3YzFjMCIsImF1ZCI6Im1vdmllLWNhc3QiLCJpYXQiOjE1ODEwNjMzMjMsImV4cCI6MTU4MTA3MDUyMywiYXpwIjoiNGd6WmJJd3FTbTJtaEJ5WGhWTFowejJUNXRSaFZwSUMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImFkZDptb3ZpZSIsImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsIm1vZGlmeTphY3RvciIsIm1vZGlmeTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.LeNjhIioVAyyh2COs5G33kavrAMxEjrlY6iDr54kOijFVIkl0Jb_uLkX--Y_fXhyt5reVArvshGXOEj0Tfqrt4xOKBWcDboAa3WDdmRwboXZfYk79VIGtmNd-fn6yN6kcQoNBM9kAOKg410dJma3D1R-uoLrbdZIH4GMaBFg9omN9irmEGjapPv0Fxks5twbA1Y1lmI00QXa8KqKjBqC6mckcDbhW_lw1XgHj6Os63IYrUG-jn8NsPt4vcEWmlZHZ9kk9vrnutYRJ18EFR9LEGq2hgI-HpbqlZmfAIal9FWeoksa0LvyUM0BPpUPc9V9tXg4WyJzCTM3wefwyog_eg'
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFUSkJORE5ETWtWQ09UTkJOVUpCUlRBd05VRTVRVGd4TmpjMU5FUTJOekF5T1RWRU5qRkVOUSJ9.eyJpc3MiOiJodHRwczovL3VraHUtbW92aWUtY2FzdC1hcGkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2M4OTM0MTEwNGFjMGVhMDUxOTQ3NSIsImF1ZCI6Im1vdmllLWNhc3QiLCJpYXQiOjE1ODEwNjM1NDQsImV4cCI6MTU4MTA3MDc0NCwiYXpwIjoiNGd6WmJJd3FTbTJtaEJ5WGhWTFowejJUNXRSaFZwSUMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvciIsImRlbGV0ZTphY3RvciIsIm1vZGlmeTphY3RvciIsIm1vZGlmeTptb3ZpZSIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.hXAI9slmb3COWhHV3dIyLqKyT_op790vpuaNFHUCDKtNIRTqAXwfzdsnYpONLXST_8SoFekzzQy2efKa2y9xrTI0wjhYCeQYaVCEAshbFULJHG-J-6zuGALYrUOIDjisn86XZ1TsXOBQlzZlCw6EqMGYSK_GXvN3qOZXQkd5rOx_XIJZ36jF9clXtY3nwFCyQudo1X9RQ_I6BXQhezYwOCzENmvxtWGHeEjYc8FMmMBcuHgUC4Dc98yDWhZ2ZaMmIvMHhObIvtjp4GVCyOuHoxGqcUOnUH5DSZDwLQoddw4hyEjYBXCQ20UR4u1Q3UuFuQdlhb0uTaqxVdYubq86AA'
CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFUSkJORE5ETWtWQ09UTkJOVUpCUlRBd05VRTVRVGd4TmpjMU5FUTJOekF5T1RWRU5qRkVOUSJ9.eyJpc3MiOiJodHRwczovL3VraHUtbW92aWUtY2FzdC1hcGkuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlM2M4Yjk3MzNmZGYzMGU5YWNjY2Y2YyIsImF1ZCI6Im1vdmllLWNhc3QiLCJpYXQiOjE1ODEwNjM1ODUsImV4cCI6MTU4MTA3MDc4NSwiYXpwIjoiNGd6WmJJd3FTbTJtaEJ5WGhWTFowejJUNXRSaFZwSUMiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.N5OOVAMGQovoxnBBdk5DrKzOGW2CfgJQcF9MQ4VMLniJwnq1zSeDQXyPm3wXiBLxyPh3k7SJU7xv0Cgk_Z8qw-Nlshl5IlDOvSg2bu97Kev1ndPCeajMTNN-zDw-AorzexTBTNdSQjb_x_b5VeCnukED1b6UKpcBhBpRRIE8D-JQwy2VT4FaSqAqfukFskKAWgL5GsonemF27DDUvMjmLOBfzxa8GWj-1UL-9BWLrQCNoi7P5alrAJE6AgBVw0BcImKt5HEahO71Ie4jJ3WnnJn9Ea2unBitHxp_rC3jK9JntDeQGR2p26kUlXWg_-jdtyqRxrrFuh-1UrLLJtLQcA'

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
