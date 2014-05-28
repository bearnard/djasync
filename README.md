# Django async webserver

A Proof Of Concept, an exercise implemntation of an `asyncio`-based WSGI
webserver for django.

Also contains a half-cooked HTTP parser made with python generators.


## Running tests

`py.test`


## Running a django app

Create the app:

     django-admin.py startproject testapp

Run the asyncserver

	PYTHONPATH=testapp python -m djasync.webserver --host localhost --port 8000 testapp.wsgi.application


## Developer setup

1. install pyenv
2. install python 3.4:

    pyenv install 3.4.0 && pyenv local 3.4.0

3. create virtualenv:

    pyvenv virtual

4. activate virtualenv

	source virtual/bin/activate

5. install required python packages

	pip install -r requirements.txt

