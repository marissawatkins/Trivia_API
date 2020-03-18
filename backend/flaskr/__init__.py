import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def pagination_questions(request, questions):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  quizzes = [play_quiz.format() for play_quiz in questions]
  current_questions = quizzes[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
  #Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs

  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    return response
  #Use the after_request decorator to set Access-Control-Allow

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.all()
    formatted_category = {category.id: category.type for category in categories}

    return jsonify({
      'categories': formatted_category,
      'status': 200
    })
  # Create an endpoint to handle GET requests for all available categories.

  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    questions = Question.query.order_by(Question.id).all()
    categories = Category.query.order_by(Category.id).all()
    current_questions = pagination_questions(request, questions)
    formatted_categories = {category.id: category.type for category in categories}
    categories = list(map(Category.format, Category.query.all()))

    # total_questions = len(questions)

    if len(current_questions) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formatted_categories,
      'current_category': None
    }) 
  # Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
  # This endpoint should return a list of questions, number of total questions, current category, categories. 

  # TEST: At this point, when you start the application
  # you should see questions and categories generated, ten questions per page and pagination at the bottom of the screen for three pages.
  # Clicking on the page numbers should update the questions. 

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()

      if not question:
        abort(404)
      question.delete()
      
      return jsonify({
        'success': True
      })

    except:
      abort(422) #400
  # Create an endpoint to DELETE question using a question ID. 

  # TEST: When you click the trash icon next to a question, the question will be removed.
  # This removal will persist in the database and when you refresh the page. 

  @app.route('/questions', methods=['POST'])
  def create_question():
    request_body = request.get_json()
    question = request_body.get('question', '')
    answer = request_body.get('answer', '')
    category = request_body.get('category', '')
    difficulty = request_body.get('difficulty', '')

    if ((question == '') or (answer == '') or (difficulty == '') or (category == '')):
      abort(422)
    try:
      question = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      question.insert()

      questions = Question.query.order_by(Question.id).all()
      current_questions = pagination_questions(request, questions)
      total_questions = len(questions)

      return jsonify({
        'success': True,
        'created': quesiton.id,
        'questions': current_questions,
        'total_question': total_questions,
        'message': 'Question successfully created!'
      }), 200

    except: 
      abort(422)
  # Create an endpoint to POST a new question, 
  # which will require the question and answer text, 
  # category, and difficulty score.

  # TEST: When you submit a question on the "Add" tab, 
  # the form will clear and the question will appear at the end of the last page
  # of the questions list in the "List" tab.  

  # @app.route('/questions/search', methods=['POST'])
  # def search():
  #   body = request.get_json()
  #   search_term = body.get('searchTerm', '')

  #   if search_term == '':
  #     abort(422)

  #   try:
  #     questions = Question.query.filter(Question.question.ilike(f'%{search_term}%'))

  #     if len(questions) == 0:
  #       abort(404)

  #     pagination_questions = get_paginated_questions(request, questions, QUESTIONS_PER_PAGE)

  #     return jsonify({
  #       'success': True,
  #       'questions': pagination_questions,
  #       'total_quesitons': len(Question.query.all())
  #     }), 200

  #   except:
  #     abort(404)
    # body = request.get_json()
    # search_term = body.get('searchTerm', None)

    # if search_term:
    #   search_results = Question.query.filter(Question.question.ilike('%{search_term}%')).all()

    #   return jsonify({
    #     'success': True,
    #     'questions': [question.format() for question in search_results],
    #     'total_quesitons': len(search_results),
    #     'current_category': None
    #   })
    # abort(404)

  # @TODO: 
  # Create a POST endpoint to get questions based on a search term. 
  # It should return any questions for whom the search term is a substring of the question. 
  # TEST: Search by any phrase. The questions list will update to include only question that include that string within their question. 
  # Try using the word "title" to start. 

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    questions = Question.query.filter_by(category = category_id).all()
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions) == 0:
      abort(404)
    
    return jsonify({
      'questions': formatted_questions,
      'total_questions': len(formatted_questions),
      'current_category': category_id
    })
  # except:
  #   abort(405)
  
  # Create a GET endpoint to get questions based on category. 
  # TEST: In the "List" tab / main screen, clicking on one of the categories in the left column will cause only questions of that category to be shown. 


  @app.route('/quizzes', methods=['POST'])
  def quizzes():
    try:
      data = request.get_json()
      # check given category
      category_id = int(data["quiz_category"]["id"])
      category = Category.query.get(category_id)
      previous_questions = data["previous_questions"]
      if not category == None:  
        if "previous_questions" in data and len(previous_questions) > 0:
          questions = Question.query.filter(
            Question.id.notin_(previous_questions),
            Question.category == category.id
            ).all()  
        else:
          questions = Question.query.filter(Question.category == category.id).all()
      else:
        if "previous_questions" in data and len(previous_questions) > 0:
          questions = Question.query.filter(Question.id.notin_(previous_questions)).all()  
        else:
          questions = Question.query.all()
      max = len(questions) - 1
      if max > 0:
        question = questions[random.randint(0, max)].format()
      else:
        question = False
      return jsonify({
        "success": True,
        "question": question
      })
    except:
      abort(500, "An error occured while trying to load the next question")

  # Create a POST endpoint to get questions to play the quiz. 
  # This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
  # TEST: In the "Play" tab, after a user selects "All" or a category, one question at a time is displayed, the user is allowed to answer and shown whether they were correct or not. 

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Not found"
    }), 404

  @app.errorhandler(405)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 405,
      "message": "bad request" 
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable"
    }), 422

  @app.errorhandler(500)
  def restricted(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": "Internal Error"
    }), 500
    # Create error handlers for all expected errors 
    # including 404 and 422. 
  
  return app

    