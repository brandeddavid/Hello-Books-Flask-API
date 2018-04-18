# Hello-Books-Flask-API
[![Build Status](https://travis-ci.org/brandeddavid/Hello-Books-Flask-API.svg?branch=master)](https://travis-ci.org/brandeddavid/Hello-Books-Flask-API)
[![Coverage Status](https://coveralls.io/repos/github/brandeddavid/Hello-Books-Flask-API/badge.svg?branch=master)](https://coveralls.io/github/brandeddavid/Hello-Books-Flask-API?branch=master)

This repository contains Flask API endpoints and tests for the Hello-World Application.

## Runnning Application
Clone Repo From GitHub
```
git clone https://github.com/brandeddavid/Hello-Books-Flask-API.git
```
Enter Directory
```
cd Hello-Books-Flask-API
```
Create Virtual Environment
```
virtualenv -p python3 venv
```
Start virtualenv
```
source venv/bin/activate
```
Install Dependencies
```
pip install -r requrements.txt
```
Run app
```
python run.py
```

## Available API Endpoints

| Endpoint | Description |
| --- | --- |
| POST /api/v1/books | Adds a New Book
| PUT /api/v1/books/<string:bookId> | Edits Individal Book Info
| DELETE /api/v1/books/<string:bookId> | Deletes A Book
| GET /api/v1/books | Retrieves All Books
| GET /api/v1/books/<string: bookId> | Get Book by id
| POST /api/v1/users/books/<string: bookId> | Borrow a book
| POST /api/v1/auth/register | Register a New User
| POST /api/v1/users | Gets all Users
| POST /api/v1/auth/login | Logs in a registered User
| POST /api/v1/auth/logout | Logs Out a Logged in 

## API Endpoints Documentation

Find API endpoints documentation [here](https://banana-pie-71385.herokuapp.com/)

## Testing API Endpoints

Use Postman and the provided documentation to test the API endpoints


## Project Owner 

David Mwangi Mathenge

[david.mathenge98@gmail.com](mailto:david.mathenge98@gmail.com)
