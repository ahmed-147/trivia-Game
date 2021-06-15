import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# -------------------------questions per page ------------------
def get_paginated_questions(request, questions, num_of_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * num_of_questions
    end = start + num_of_questions

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions
# ----------------------------------
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  
  # CORS(app,resorces={'/' :{'origins':'*'} })
  cors = CORS(app ,resorces={r'/*' :{'origins':'*'} })
  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    
    response.headers.add('Access-Control-Allow-Credentials','true')
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,PATCH,POST,DELETE,OPTIONS')
    return response
  
  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    
    try:
      # get from Category table all records
      categories = Category.query.order_by(Category.id).all()
      categs = {}

      # list the categories to match requirement of the frontend 
      for cat in categories:
        categs[cat.id] = cat.type

      # return the requirements as json to the client   
      return jsonify({
                'success': True,
                'categories': categs
            }), 200
    except:
      abort(400)

  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_questions():
    
    # get from Category and Question table all records
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    categs = {}

    # list the categories to match requirement of the frontend 
    for cat in categories:
      categs[cat.id] = cat.type

    #  get the questions per page 
    current_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)
    
    # check the get_paginated_questions return 
    if (len(current_questions) == 0):
      abort(404)
    
    # return the requirements as json to the client 
    return jsonify({
      'success': True,
      'questions' : current_questions ,
      'total_questions' : len(questions),
      'categories': categs,
      'current_category': ''
      }), 200

  
  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error = False 
    try:
      # get from Question table the record that belong to this Id    
      ques = Question.query.filter(Question.id == question_id).one()
      # check if this question existing 
      if ques is None:
        abort(404)
        error = True 
      else:
        #delete the question 
        ques.delete()
    except:
      abort(422)
    # return the requirements as json to the client
    return jsonify({
        'success': True,
        'message': "Question was deleted"
      }),200
  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def set_question():
    # get the request json data 
    body = request.get_json()

    new_question = body.get('question', '')
    new_answer = body.get('answer', '')
    new_difficulty = body.get('difficulty', 0)
    new_category = body.get('category', '')

    # check json data 
    if not new_question or not new_answer or not new_difficulty or not new_category:
      abort(422)
    try:
      # create new question 
      qu = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
      qu.insert()
      # return the requirements as json to the client
      return jsonify({
        'success': True,
        'message': "Question was created"
        }), 201
    except:
      abort(422)
    
  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/searchs', methods=['POST'])
  def get_search_questions():
    # get the request json data 
    body = request.get_json()

    #  check the json data
    if not body.get('searchTerm', '') :
      abort(422)

    search_term = '%'+body.get('searchTerm', '')+' %'

    try:
      # get the question that have this search term 
      questions = Question.query.filter(Question.question.ilike(search_term)).order_by(Question.id).all()
      
      if not questions:
        abort(404)

      #  get the questions per page 
      current_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)

      #  check the get_paginated_questions return  
      if (len(current_questions) == 0):
        abort(404)
      
      # return the requirements as json to the client
      return jsonify({
        'success': True,
        'questions' : current_questions ,
        'total_questions' : len(questions),
        'current_category': ''
        }), 200
    except:
      abort(404)
    

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_specific_questions(category_id):
    # convert Id to string 
    c_id = str(category_id)

    # get the questtions that belong to this category Id that returned from the URl
    questions = Question.query.filter(Question.category==c_id).order_by(Question.id).all()
    
    # check the return 
    if not questions:
      abort(404)
    
    current_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)
    # get the category that belong to this Id 
    categ = Category.query.filter(Category.id==category_id).all()

    if not categ:
      abort(404)
    
    categs = {}

    for cat in categ:
      categs[cat.id] = cat.type
    
    # return the requirements as json to the client
    return jsonify({ 
      'success': True,
      'questions' : current_questions ,
      'total_questions' : len(questions),
      'current_category': categs[category_id]
      }), 200
    

  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_quizzes():

    # function to get random question 
    def get_random_question(questions):
      return questions[random.randint(0, len(questions)-1)]
    # get the data 
    body = request.get_json()

    if not body :
      abort(404)
    
    previous_questions = body.get('previous_questions', None)
    quiz_category = body.get('quiz_category', None)

    # check the 'quiz_category' , 'previous_questions'
    if ((quiz_category is None) or (previous_questions is None)):
      abort(400)
    
    # get random question by the chosen category  
    if quiz_category['id'] == 0:
      questions = Question.query.order_by(Question.id).all()
      next_question = get_random_question(questions)
    else:
      categ_id = str(quiz_category['id'])
      questions = Question.query.filter_by(category=categ_id).order_by(Question.id).all()
      next_question = get_random_question(questions)

    if not next_question:
      abort(404)


    # for non repeated questions 
    found = True
    while found:
      if next_question.id in previous_questions:
        next_question = get_random_question(questions)
        # print('repeated que {}'.format(next_question.format()))
      else:
        # print('non repeated que {}'.format(next_question.format()))
        found = False

    
    return jsonify({
      'success': True,
      'question' : next_question.format()
      }), 200
    
  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  # error handler for bad requset 
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request error'
    }), 400

  # error handler for Resource not found
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  # error handler for internal server error 
  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'An error has occured, please try again'
    }), 500

  #  error handler for unprocesable entity 
  @app.errorhandler(422)
  def unprocesable_entity(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable entity'
    }), 422


  return app

    