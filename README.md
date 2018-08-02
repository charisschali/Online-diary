# Online Diary V-2

[![Build Status](https://travis-ci.org/charisschomba/Diary.svg?branch=Refactor-Tests)](https://travis-ci.org/charisschomba/Diary)
[![Coverage Status](https://coveralls.io/repos/github/charisschomba/Diary/badge.svg?branch=Refactor-Tests)](https://coveralls.io/github/charisschomba/Diary?branch=Refactor-Tests)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4b7ac2f6873e46be8bfc34ec0efbfd7f)](https://www.codacy.com/app/charisschomba/Diary?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=charisschomba/Diary&amp;utm_campaign=Badge_Grade)

MyDiary is an online journal where users can pen down their thoughts and feelings.

Documentation: https://mydiaryrestapi.docs.apiary.io/

Heroku Link: https://mydiary-v2.herokuapp.com/

Endpoints

| Functionality        |    Method     |         Endpoint               |
| :------------------- |:-------------:| ------------------------------:|
| Get all entries      | GET           | /mydiary/v1/entries            |
| Get specific entry   | GET           | /mydiary/v1/entries/id         |
| Add an entry         | POST          | /mydiary/v1/entries            |
| Modify an entry      | PUT           | /mydiary/v1/entries/id         |
| Delete an entry      | DELET         | /mydiary/v1/entries/id         |
| Register             | POST          | /mydiary/v1/auth/register      |
| Login                | POST          | /mydiary/v1/auth/login         |


Requirements

- [Python3](https://www.python.org/) (programming languag)
- [Flask](http://flask.pocoo.org/) (Python webframework)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)(To isolate Api modules)
- [Pytest](https://docs.pytest.org/en/latest/) (Tool for testing)

How to setup it up:

To set it up in your machine:

1.sudo install python3

2.pip install virtualenv

Clone this repository:

git clone https://github.com/charisschomba/Diary.git

cd Diary/challenge3/

Create a virtual environment in the root directory:

virtualenv [name of virtualenv]

Activate the virtualenv:

source [name of virtualenv]/bin/activate

On your terminal run:

pip install -r requirements.txt
to install the modules

On your terminal run:

  export FLASK_APP="run.py"
  export FLASK_CONFIG="production"
  export JWT_SECRET_KEY="any random long string"
  export DB_HOST="localhost"
  export DB_NAME="database name"
  export DB_USERNAME="db user"
  export DB_PASSWORD="password"
  export SECRET_KEY="any random long string"

Run the application:

flask run

To run tests:

pytest
