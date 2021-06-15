import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category




class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','root','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #  ----------------------categories methods -----------------------------
    # test the get categories 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])       

    #    ----------------------questions methods -----------------------------
    # test the get questions
    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        

    # test the get questions with Number not found (error)  
    def test_404_pagenation_get_questions(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')
    
    # test the delete questions with id  
    def test_deleting_question(self):
        res = self.client().delete('/questions/50') # put the id of the question you want to delete it 
        data = json.loads(res.data)

        deleted_q = Question.query.filter_by(id=50).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_q, None)
    
    # test the delete questions with id not exist (error) 
    def test_422_deleting_question_nonexist_id(self):
        res = self.client().delete('/questions/10000') # put the id of the question you want to delete it 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')
    
    # test the insert question with 
    def test_post_requesting_insert_question(self):
        res = self.client().post('/questions', json={'question':'Is the moon exist ?','answer' : 'Yes' , 'difficulty': 1 ,'category': 1 }) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        

    
    # test the insert question without question and answer 
    def test_422_post_requesting_insert_question(self):
        res = self.client().post('/questions', json={'question':'','answer' : '' , 'difficulty': 1 ,'category': 1 }) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    # test the search question with search term
    def test_post_requesting_search_question(self):
        res = self.client().post('/questions/searchs', json={'searchTerm':'title'}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        
        
    # test the search question with empty search term  
    def test_422_post_requesting_insert_question(self):
        res = self.client().post('/questions/searchs', json={'searchTerm':''}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    
    # test the search question with nonexist search term  
    def test_404_post_requesting_insert_question(self):
        res = self.client().post('/questions/searchs', json={'searchTerm':'kjsdhkash'}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # test the get questions in a specific existing category  
    def test_get_specific_questions(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
        

    # test the get questions in not existing category  (error)  
    def test_404_get_specific_questions(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

# -----------------------test quizzes (/play)------------------
    # test the quizzes 
    def test_post_requesting_quizzes(self):
        client_json={
            'previous_questions':[11],
            'quiz_category':{
                'type': 'click', 
                'id': 0
                } 
        }
        res = self.client().post('/quizzes', json=client_json) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
        
    # test the quizzes   (eror)  
    def test_404_post_requesting_quizzes(self):
        res = self.client().post('/quizzes') 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()