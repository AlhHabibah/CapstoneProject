## live URL:
 https://habibah-capstone-project1.herokuapp.com/
# Motivation for the project:
This is the last project of the Udacity-Full-Stack-Nanodegree Program. It covers following technical topics in 1 app:

Database modeling was done with PostgreSQL & SQLAlchemy (see the models.py file)
An API that performs CRUD operations on database with the Flask Framework (see the app.py file)
There are also automated tests provided with Unittest (see the test_app file)
Authorization & Role based Authentification was made with the help of Auth0 and its services (see the auth.py file)
Final goal to deploy to Heroku platform.

## Installing Dependencies for the Backend
Python 3.7 - Follow instructions to install the latest version of python for your platform in the python docs

## Virtual Enviornment:
 - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

Here we initialize and activate a virtualenv:
    $ cd YOUR_PROJECT_DIRECTORY_PATH/
    $ virtualenv --no-site-packages env
    $ source env/bin/activate

# PIP Dependencies:
 - Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

    pip install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

# Key Dependencies
    Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.
## Run the following commands to install them:
```
pip install flask_script
pip install flask_migrate
pip install psycopg2-binary
```

## Running the server

1-setting up the database url as postgresql://{username}:{user Password}@{host}:{port number}/{database name}

2-first ensure you are working using your created virtual environment.
3- seting up all virtual environments.


To run the server, execute:
```
$ source setup.sh
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run
```
### To run our local migrations using our manage.py, we write:
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
Sourcing setup.sh sets some environment variables used by the app.

Setting the FLASK_ENV variable to development will detect file changes and restart the server automatically.

Setting the FLASK_APP variable to app.py directs flask to use the this file to find the application.

## Models:
Movies model defined with attributes title and release date 
Actors model defined with attributes name, age and gender
You can find the models in models.py file. Local Postgres DATABASE details are available in setup.sh file for reference.

## Endpoints
### Movies
#### GET /movies
##### Public
Fetches all the movies from the database
Request arguments: None
Returns: A list of movies contain key:value pairs of id, title and release_date
##### Response
```{
  "success": true,
  "movie": [ {
    "id" : 1,
    "title": "Star Wars",
    "duration": 120,
    "release_year": "1971"
  }, {
    "id" : 2,
    "title": "Star Wars",
    "duration": 120,
    "release_year": "1971"
  }]
}
```
#### POST /movies
Executive Producer
Creates a movie from the request's body
Request arguments: None
Returns: the created movie contains key:value pairs of id, title and release_date
##### Body
```
{
  "title": "Star Wars",
  "duration": 120,
  "release_year": "1971"
}
```
##### Response
```{
  "success": true,
  "movie": [{
    "title": "Star Wars",
    "duration": 120,
    "release_year": "1971"
  }]
}
```
#### PATCH /movies/<int:id>
Casting Director or Executive Producer
Updates a movie using the information provided by request's body
Request arguments: Movie id
Returns: the updated movie contains key:value pairs of id, title and release_date
##### Body
```{

  "duration": 150
}
```
##### Response
``` {
  "success": true,
  "movie": [{
    "title": "Star Wars",
    "duration": 150,
    "release_year": "1971"
  }]
```
#### DELETE /movies/<int:id>
Executive Producer
Deletes a movie based the request argument
Request arguments: Movie id
Returns: the deleted movie id
##### Response
```{
  "success": true,
  "deleted": 1
}```
### Actors
#### GET /actors
##### Public
Fetches all the actors from the database
Request arguments: None
Returns: A list of actors contain key:value pairs of id, name, age and gender
##### Response
```{
  "success": true,
  "actor": [
    {
      "id": 1,
      "name": "James",
      "gender": "M", 
      "age": "25"
    },
    {
       "id" : 2
       "name": "Nicholas",
       "gender": "M",
       "age":"30"
    }
  ]
}
```
#### POST /actors
Casting Director or Executive Producer
Creates an actor from the request's body
Request arguments: None
Returns: the created actor contains key:value pairs of id, name, age and gender
##### Body
```{
   "name": "Nicholas",
   "gender": "M",
   "age":"20"
}
```
##### Response

``` {
  "success": true,
  "actor": [{
     "id": 1,
     "name": "Nicholas",
     "gender": "M",
     "age": "29"
  }]
}
```
#### PATCH /actors/<int:id>
Casting Director or Executive Producer
Updates a actor using the information provided by request's body
Request arguments: Actor id
Returns: the updated actor contains key:value pairs of id, name, age and gender
##### Body
```{
   "age: "40"
}
```
##### Response
```{
  "success": true,
  "actor": [{
     "id": 1,
     "name": "Nicholas",
     "gender": "M";
     "age:"40"
  }]
}
```
#### DELETE /actors/<int:id>
Casting Director or Executive Producer
Deletes an actor based the request argument
Request arguments: Actor id
Returns: the deleted actor id
##### Response
```
{

  "success": true,
  "deleted": 1
}
```
## Error Handling
Errors are return as JSON format in the following format:
```
    {
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }
```
### The API will return six (6) error types when a request fails:
    401: "Unauthorized"
    403: "Access Denied/Forbidden"
    404: "Not found"
    405: "Method not Allowed"
    422: "unprocessable"
    500: "Internal Server Error"
        
        
       
## Auth0 Setup:
AUTH0_DOMAIN, ALGORITHMS and API_AUDIENCE are all available in the setup.sh file for reference.

Roles: All 3 roles have been defined in Auth0 and following permissions as shown for each role below are also defined in Auth0.

## Roles:
   ### Casting Assistant:
       Can view actors and movies
   ### Casting Director:
       All permissions a Casting Assistant has and…
       Add or delete an actor from the database
       Modify actors or movies
   ### Executive Producer
        All permissions a Casting Director has and…
        Add or delete a movie from the database

## Testing:
We can run our entire test case by running the following command at command line
```
$ dropdb castagency
$ createdb castagency
$ psql castagency < db.psql
$ python test_app.py
```
