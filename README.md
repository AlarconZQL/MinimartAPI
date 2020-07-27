# MinimartAPI

A simple restful API built with python and flask.

- Install dependencies: inside root project folder, execute "pip install -r requirements.txt" on your terminal

- Run server locally: inside root project's folder, execute "flask run" on you terminal and visit http://localhost:5000/ on a web browser to interact with the API

- Run application unit tests and get a test coverage report: execute "run_tests.sh" script

- To initialize database information: make a GET request to "/setup" application's endpoint (current database's tables will be dropped)
