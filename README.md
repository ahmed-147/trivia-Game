# Trivia API

Trivia api is a web application that allows people to hold trivia on a regular basis using a web page to manage the trivia app and play the game.

The app allows :

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started with the Backend

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

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

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
## Getting Started with the Backend

#### Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

#### Installing project dependencies

This project uses NPM to manage software dependencies. 

```bash
npm install
```

>_tip_: **npm i** is shorthand for **npm install**

## Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```
# API Reference

## Getting Started 
- Backend Base URL: http://127.0.0.1:5000/
- Frontend Base URL: http://127.0.0.1:3000/
- Authentication: Authentication or API keys are not used in the project yet.

## Error Handling
Errors are returned in the following json format:

```bash
{
"success": "False",
"error": 422,
"message": "Unprocessable entity",
}
```
The error codes currently returned are:

- 400 – bad request
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error

## Endpoints

### GET /categories
- General:
    1. Returns all the categories.

- Sample: curl http://127.0.0.1:5000/categories
```bash
    {
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

### GET /questions
- General:
    1. Returns all questions
    2. questions are in a paginated.
    3. pages could be requested by a query string

- Sample: curl http://127.0.0.1:5000/questions
```bash
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": "5", 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": "5", 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": "4", 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": "5", 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": "4", 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": "6", 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": "6", 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": "3", 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": "3", 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 43
}
```

### Delete /questions/<int:question_id>
- General:
    1. Delete the question that have this ID.

- Sample: curl -X DELETE http://127.0.0.1:5000/questions/42
```bash
{
  "message": "Question was deleted",
  "success": true
}
```
### Post /questions
- General:
    1. Creates a new question based on a payload

- Sample: curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "How many paintings did Van Gogh sell in his lifetime?", "answer": "One", "difficulty": 4, "category": "2" }'
```bash
{
    "message": "Question was created",
    "success": true
}
```
### Post /questions/searchs
- General:
    1. Returns all questions that have this `searchTerm`
    2. Return total of questions include this search Term


- Sample: curl -X POST http://127.0.0.1:5000/questions/searchs -H "Content-Type: application/json" -d '{"searchTerm": "what"}'
```bash
{
    "current_category": "",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": "5",
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": "5",
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": "5",
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Lake Victoria",
            "category": "3",
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Liver",
            "category": "1",
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        }
    ],
    "success": true,
    "total_questions": 6
}
```
### GET /categories/<int:category_id>/questions
- General:
    1. Returns all questions in specific  category by `category_id` that send with URL
    2. Return category name
    3. Return the total questions in this category

- Sample: curl http://127.0.0.1:5000/categories/1/questions
```bash
{
    "current_category": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": "4",
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": "4",
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "George Washington Carver",
            "category": "4",
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Scarab",
            "category": "4",
            "difficulty": 4,
            "id": 23,
            "question": "Which dung beetle was worshipped by the ancient Egyptians?"
        },
        {
            "answer": "sad",
            "category": "4",
            "difficulty": 2,
            "id": 30,
            "question": "ali"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

### Post /quizzes
- General:
    1. play game.
    2. Returns random question (in specific category if there is chosin category by `category_id` that send with URL ) 
    3. Return category name
    4. Return the total questions in this category

- Sample choes from all categories: curl -X POST http://127.0.0.1:5000/quizzes -H "Content-Type: application/json" 
-d '{"previous_questions": [],"quiz_category": {"type":"Click","id":0}}'
```bash
{
    "question": {
        "answer": "Jackson Pollock",
        "category": "2",
        "difficulty": 2,
        "id": 19,
        "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    "success": true
}
```

# Authors
- Ahmed Fathi Khalifa worked on the API and test suite to integrate with the frontend
- Udacity provided the starter files for the project including the frontend