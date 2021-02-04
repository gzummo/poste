### Setup
 * Install python 3.7 & pipenv
 * `pipenv install` to install project's requirements
 * Install Redis or `docker run -d -p 6379:6379 redis`

### Run
#### Flask server
 * `pipenv shell` to enter virtual environment (loading the variables in .env)
 * `flask run`

#### Redis
 * In a second terminal, go to your Redis directory and enter `src/redis-server`

#### Celery worker
 * In a third terminal, enter virtual environment with `pipenv shell` and enter `celery -A app.celery worker --loglevel=INFO`

#### Postman
 * Import _poste_._postman__collection_._json_ to Postman and try the endpoints.

### Endpoints
 `POST http://localhost:5000/letter/`

 Will get fetch the status of a letter and update it in database.

 * Parameters: 
  * letter_id, string (required). Example : "3C00638101810". The identifier of the letter you want a status from.

`POST http://localhost:5000/letter/update_all`

 Will update the status of every letter in database asynchronously and return a _task__id_ to follow the progress.

`GET http://localhost:5000/letter/task/<task_id>`

Will return the progress status of celery task and its result if it is done.

### Explore DB
Database is running on SQLite, it can be browsed using "DB Browser for SQLite" or you can run a shell with `sqlite3 test.db` if sqlite3 is installed.