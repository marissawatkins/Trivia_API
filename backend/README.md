# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
```bash
py -m pip --version
py -m pip install --upgrade pip
or
py -m pip install --user virtualenv
```
Create virtual env by:
```bash
py -m venv env
```
Activate env by:
```bash
cd into env folder
cd into Scripts
. activate 
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql -U postgres
create database trivia
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Endpoints
GET '/categories'
GET '/questions'
POST '/questions'
DELETE '/questions/<int:question_id>'
POST '/questions/search'
GET '/categories/<int:category_id>/questions'
POST '/quizzes'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

GET '/questions'
- Returns a list of questions, number of total questions, current category, categories. 
- Request Arguments: None
- Returns:
```
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports
        },
        "current_category": null,
        "questions": [
            {
                "answer": "Apollo 13",
                "category": 5,
                "difficulty": 4,
                "id": 2,
                "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
            },
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            }
        ], 
        "success": true,
        "total_questions": 
    }
```

POST '/questions'
- Submits a new question to the database 
- Request Arguments: Question, answer, category, difficulty
- returns:
```
    {
        "questions": {
        "question": "What color is the sky?",
        "answer": "Blue",
        "difficulty": 1,
        "category": 1
        },
        "status": 200,
        "success": true
    }
```

DELETE '/questions/<int:question_id>'
- Deletes a question
- Returns: Success with status code of 200 when successfully deleted. If not, 404 or 422 when not successful
- Parameters: <int:question_id>
```
    {
        "success": true
    }
```

POST '/questions/search'
- Returns any questions for whom the search term is a substring of the question. 
- Returns: Questions, total quesitons, and current category. Successful code 200 and 404 when not 
- Request Argument: Takes searchTerm
```
    {
        "searchTerm": "Maui"
    }
    {
        "categories": {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        },
    }
    {
        "current_category": null,
        "questions" : [
            {
                "answer": "Yes",
                "category": 3,
                "difficulty": 1,
                "id": 26,
                "question": "Is Maui in Hawaii?"
            }
        ],
        "success": true,
        "total_questions": 1     
    }
```

GET '/categories/<int:category_id>/questions'
- Returns questions based on category
- Parameter: <int:category_id>
- Returns:
```
    {
        
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
            "answer": "Jackson Pollock",
            "category": 2,
            "difficulty": 2,
            "id": 19,
            "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
    ],
    "success: true,
    "total_questions": 4
    }
```

POST '/quizzes'
- Allows for the quiz to be played
- Returns: Success status code 200, quesitons. If unsuccessful, will throw a 500 error
- Parameters: * category_id
              * previous_questions
```
    {
        "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    "success": true
```


##Errors

#Not Found: 404
```
    "success": False,
    "error": 404,
    "message": "Not found"
```
#Bad Request: 405
```
    "success": False,
    "error": 405,
    "message": "bad request" 
```
#Unproccessable: 422
```
    "success": False,
    "error": 422,
    "message": "Unprocessable"
```
#Internal Error: 500
```
    "success": False,
    "error": 500,
    "message": "Internal Error"
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
