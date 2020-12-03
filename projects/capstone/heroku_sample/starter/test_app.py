import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, Cast


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstonetest"
        self.database_path = "postgres://{}:{}@{}/{}".format('rhee','projectpassword','localhost:5432', self.database_name)
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            invalid_castingassistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkRlVzhQY1ZUZmdYeHVKd2t1TFBrcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc2FhZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYwY2JlNThhMWY2MDMwMDE5YjBiYjI5IiwiYXVkIjoiQ29mZmVlIHRhc3RlciIsImlhdCI6MTU5NTU0NDg0MiwiZXhwIjoxNTk1NjMxMjQyLCJhenAiOiJCQlpGRnhGZEJQRFV2bndvWjlNZmEwYkxyb1ZmSUE1SiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0Om5hbWUiLCJnZXQ6dmlzaXRlZCIsInBvc3Q6dmlzaXRlZCJdfQ.QQ0cSHSZEHVnvhzBUts59vvXJ_aPqodtNabyHHlXKq_cujkf8F60BrYPR8YDUrWwebWFKWLD2dyuH_41HgDnoNLBSkmNMY5wQSbOK8AppI_qrgXjHZNQ4ZWQDUcsJIl5gSUb8E1lEKZypVCEEg6urosk_rAnmScUiabj13ihKZ3qsTP3y27iCFa-idtiqniJPxtrbPS_uNNQR85MkDyPt87tuBFiGyDosRErKCAGil4fhe9XI-dKOVSPUf-mI2n6Yqp1vocgU-gVtSC0oS0guR0245WFRcqShb55N66iO2sRJqKly8Qws-OTQAefDkNXm01nUJ_ELFrkjgd1VHgWpg'
            castingassistant_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZNUVpCQ01DV1pzRmhoMGE5SU5scyJ9.eyJpc3MiOiJodHRwczovL2t3cmhlZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjMGJmODIxYTc1NTAwMDc2MDQ3YTgyIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwNjk3MTgwMywiZXhwIjoxNjA3MDE1MDAzLCJhenAiOiJZSXNTRDNvblNMb2hZT3oycGpna1hHVThZRGNFM2lWWSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3OmNhc3QiLCJ2aWV3Om1vdmllcyJdfQ.WFhnV2CbNFejGWn8ONmRKdG9_hQs63DbjpJKnjteFyOy26dSqO4b_kqsXppUUOYj4kqHla0yu1QkfUoYtaEZf0-2Dz7ElvDim2tnDbJxY7pFxC5wMrOVyAwcmdj3XydnCNhofNowJrsR30bSxQ4rOPs8VdrqQjwg-i6yAo83wuCieJiqIOMAmjsyIvD1OQ_Q30Jdw9fMN7_6WjkWwfVGl76pfDkVPEvqEG3pPe-0RALQOEafd-KcapPffWEQ2UxAK79itYoA7pofktByZmVA1JQkrMq1eXeSALqO-OVAJCR3NoHK8O7Hg_cWVRJD4i_iFol9dLHBLTYrjxlIwQMkyw'
            castingdirector_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZNUVpCQ01DV1pzRmhoMGE5SU5scyJ9.eyJpc3MiOiJodHRwczovL2t3cmhlZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjMGJmZWUxODY2YjQwMDY4NjhiODhjIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwNjk3MTg2OSwiZXhwIjoxNjA3MDE1MDY5LCJhenAiOiJZSXNTRDNvblNMb2hZT3oycGpna1hHVThZRGNFM2lWWSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDpjYXN0IiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTpjYXN0IiwibW9kaWZ5OmFjdG9ycyIsIm1vZGlmeTptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6Y2FzdCIsInZpZXc6bW92aWVzIl19.rb1V0dllBKIxKZ0cHEbeGxi1mUyVAjKLxX1WUaFHZjl3s3tEKYdIhUhSc6_m124uA0G4Ys8DL2f9nLtdSrCjLoTs4PyGyNLf9T9YDwS1R7ZfwlCKAV_VKpFWV9OwSu36Uah6pzqq1hZUtCI_pQbp0ZcpG1hPh54EsUYF5-j0aZMNFUPSI3cbeeYqWwLAivALkzUSgVYwHaGKukFDzXh1eiKwh8nJFadw995_GXlU5B1UBRmhKxltBOGinMGLgzM44M-ynCdNs4Wick8zGPtaCS2v3qp_1Mv4H7AOumK06nZCU4mrTPMnUBvQpksWBjxkju87E5BvJtBV1sHnaw_L_g'
            executiveproducer_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZNUVpCQ01DV1pzRmhoMGE5SU5scyJ9.eyJpc3MiOiJodHRwczovL2t3cmhlZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZjMGMwMjJiMjk0YmUwMDY5YTA4ZjFhIiwiYXVkIjoiY2FzdGluZ2FnZW5jeSIsImlhdCI6MTYwNjk3MTkyMywiZXhwIjoxNjA3MDE1MTIzLCJhenAiOiJZSXNTRDNvblNMb2hZT3oycGpna1hHVThZRGNFM2lWWSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDpjYXN0IiwiYWRkOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6Y2FzdCIsImRlbGV0ZTptb3ZpZXMiLCJtb2RpZnk6YWN0b3JzIiwibW9kaWZ5Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzpjYXN0Iiwidmlldzptb3ZpZXMiXX0.Py_FGhb3AsCddZ3nCuBc9GCFNV75fR5StVWIMOMysXoa8SBD4byNr1dmQPXCEceO6ARHXvYjTiykfnF6TEnq9gLMHSF-3upnGFZ3hXykKB1lg-2TZ4PA03Z9JKOZXOvqoqkpHYj1KmFA_ZMIm9KWWDC57sc2smbkUyUC3n6Fk0VUXO4pFq8z-My_C07czW_LIyDuUippQM0rrK3mR7CvDpBGfcmbpNHshLQaByo_hmVcBcWY3r7l5EoretZPs_BgdycsJK1kpVU6d9w3aYnPlSMsHB703AceTPJsEKjJlH8oLq8U7YbujF-XvahX5_3ZnMJuAEBWXYGOcMP404reqA'            
            self.invalid_castingassistant_header = {'Authorization': 'Bearer ' + str(invalid_castingassistant_jwt)}
            self.castingassistant_header = {'Authorization': 'Bearer ' + str(castingassistant_jwt)}
            self.castingdirector_header = {'Authorization': 'Bearer ' + str(castingdirector_jwt)}
            self.executiveproducer_header = {'Authorization': 'Bearer ' + str(executiveproducer_jwt)}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
    autherror 400, 401, ...
    error 404, 422
    '''
    def test_autherror_get_actors(self):
        res = self.client().get('/actors', headers=self.invalid_castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])

    def test_autherror_get_movies(self):
        res = self.client().get('/movies', headers=self.invalid_castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
  
    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.castingdirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])
  
    def test_add_actors(self):
        new_actor = {
            "name":"Lee Sun-kyun",
            "age":45,
            "gender":"Male"
        }

        res = self.client().post('/actors', json=new_actor, headers=self.castingdirector_header)
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name="Lee Sun-kyun", age=45, gender="Male").all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor)

    def test_autherror_add_actors(self):
        new_actor = {
            "name":"Song Hye-kyo",
            "age":40,
            "gender":"Female"
        }
        
        res = self.client().post('/actors', json=new_actor, headers=self.castingassistant_header)

        self.assertEqual(res.status_code, 401)

    def test_422_add_actors(self):
        new_actor = {
            "name":"Song Kang-ho",
            "age":53,
            "gender":"Male"
        }
        
        res = self.client().post('/actors', json=new_actor, headers=self.castingdirector_header)

        self.assertEqual(res.status_code, 422)

    def test_add_movies(self):
        new_movie = {
            "title":"OldBoy",
            "release_date":"112103"
        }

        res = self.client().post('/movies', json=new_movie, headers=self.executiveproducer_header)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(title="OldBoy", release_date="112103").all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie)

    def test_autherror_add_movies(self):
        new_movie = {
            "title":"The Handmaden",
            "release_date":"060116"
        }

        res = self.client().post('/movies', json=new_movie, headers=self.castingdirector_header)

        self.assertEqual(res.status_code, 401)
    
    def test_422_add_movies(self):
        new_movie = {
            "title":"Parasite",
            "release_date":"053019"
        }

        res = self.client().post('/movies', json=new_movie, headers=self.executiveproducer_header)

        self.assertEqual(res.status_code, 422)
    
    def test_autherror_update_actors(self):
        modified_actor = {
            "name":"Tilda Swinton",
            "age":40,
            "gender":"Female"
        }

        res = self.client().patch('/actors/4', json=modified_actor, headers=self.castingassistant_header)

        self.assertEqual(res.status_code, 401)
    
    def test_404_update_actors(self):
        modified_actor = {
            "name":"Tilda Swinton",
            "age":40,
            "gender":"Female"
        }

        res = self.client().patch('/actors/100', json=modified_actor, headers=self.castingdirector_header)

        self.assertEqual(res.status_code, 404)

    def test_update_actors(self):
        modified_actor = {
            "name":"Tilda Swinton",
            "age":40,
            "gender":"Female"
        }

        res = self.client().patch('/actors/4', json=modified_actor, headers=self.castingdirector_header)
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name="Tilda Swinton", age=40, gender="Female").all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor)
    
    def test_autherror_update_movies(self):
        modified_movie = {
            "title":"Snowpiercer",
            "release_date":"111111"
        }

        res = self.client().patch('/movies/4', json=modified_movie, headers=self.castingassistant_header)

        self.assertEqual(res.status_code, 401)

    def test_404_update_movies(self):
        modified_movie = {
            "title":"Snowpiercer",
            "release_date":"111111"
        }

        res = self.client().patch('/movies/100', json=modified_movie, headers=self.executiveproducer_header)

        self.assertEqual(res.status_code, 404)
    
    def test_update_movies(self):
        modified_movie = {
            "title":"Snowpiercer",
            "release_date":"111111"
        }

        res = self.client().patch('/movies/4', json=modified_movie, headers=self.executiveproducer_header)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(title="OldBoy", release_date="111111")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie)

    def test_autherror_delete_actors(self):
        res = self.client().delete('/actors/7', headers=self.castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_404_delete_actors(self):
        res = self.client().delete('/actors/100', headers=self.castingdirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
    
    def test_delete_actors(self):
        res = self.client().delete('/actors/7', headers=self.castingdirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_autherror_delete_movies(self):
        res = self.client().delete('/movies/7', headers=self.castingdirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_404_delete_movies(self):
        res = self.client().delete('/movies/100', headers=self.executiveproducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_movies(self):
        res = self.client().delete('/movies/7', headers=self.executiveproducer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_autherror_get_cast(self):
        res = self.client().get('/cast', headers=self.invalid_castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    def test_401_get_cast(self):
        res = self.client().get('/cast')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_get_cast(self):
        res = self.client().get('/cast', headers=self.castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['cast'])

    def test_autherror_add_cast(self):
        new_cast = {
            "movie_id":1,
            "actor_id":5,
            "role":"Joker"
        }

        res = self.client().post('/cast', json=new_cast, headers=self.castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_404_add_cast(self):
        new_cast = {
            "movie_id":100,
            "actor_id":5,
            "role":"Joker"
        }

        res = self.client().post('/cast', json=new_cast, headers=self.castingdirector_header)

        self.assertEqual(res.status_code, 404)

    def test_add_cast(self):
        new_cast = {
            "movie_id":1,
            "actor_id":5,
            "role":"Joker"
        }

        res = self.client().post('/cast', json=new_cast, headers=self.castingdirector_header)
        data = json.loads(res.data)

        cast = Cast.query.filter_by(movie_id=1, actor_id=5, role="Joker").all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(cast)       

    def test_autherror_delete_cast(self):
        res = self.client().delete('/cast/7', headers=self.castingassistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

    def test_404_delete_cast(self):
        res = self.client().delete('/cast/100', headers=self.castingdirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_delete_cast(self):
        res = self.client().delete('/cast/7', headers=self.castingdirector_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

