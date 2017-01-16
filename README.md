# Loki Project

  [![Build Status](https://travis-ci.org/HackSoftware/Loki.svg?branch=master)](https://travis-ci.org/HackSoftware/Loki)
  [![Coverage Status](https://coveralls.io/repos/HackSoftware/Loki/badge.svg?branch=master)](https://coveralls.io/r/HackSoftware/Loki?branch=master)


Loki is son of Odin. That project stores all the data of HackBulgaria.
It takes care of all the courses and HackFMI! It is developed by HackBulgaria Software team!

Local development setup
-----------------------

The project is using:

-   Python 3.5
-   Django 1.9

In order to setup it, there are the following steps:

-   Install python requirements:

<!-- -->

    $ pip install -r requirements/base.txt

-   Setup Postgres

<!-- -->

    $ sudo -u postgres createuser your_postgres_username
    $ sudo -u postgres createdb -O your_postgres_username your_postgres_database_name

-   Setup local environment variables


There is an [example_env_variables](example_env_variables) file, from which you can see the exact environment variables you need to export.


-   Run migrations

<!-- -->

    $ python manage.py migrate

-   Run server

<!-- -->

    $ python manage.py runserver

-   Install node

<!-- -->

    Follow the https://nodejs.org/en/download/ in oder to download the latest version of npm and nodejs.

-   Install bower

<!-- -->

    $ sudo npm install -g bower
    $ cd loki/website/static
    $ bower install bower.json


Celery
------

This project is using Celery for async tasks such as email sending and working with Grader API.

In order to run Celery, you are going to need **RabbitMQ Server**

The following variables are taking care of everything, you just have to export it:

    export BROKER_URL="amqp://guest:guest@localhost//"

Afer that, you can run Celery:

    $ celery -A loki worker -B

Grader
------

We use [Grader](https://github.com/HackBulgaria/HackTester) in order to test the solution sent by student. In order to use the Grader API you need to set values
to the following variables:

    export GRADER_ADDRESS="grader-address"
    export GRADER_API_KEY="grader-api-key"
    export GRADER_API_SECRET="your-grader-api-secret-key"


Running tests
--------------

Before running the tests, you need to install the right requirements for them:
    
    $ pip install -r requirements/test.txt
  
In order to run the tests, choose whichever command you prefer:

    $ python manage.py test

    $ py.test


***In case you get permission error:***

Since the local database we use is Postgres, the tests try to create
their own database,so you need to grant the Postgres user with CREATEDB
permission:

    $ sudo -u postgres psql
    postgres=# ALTER USER username CREATEDB;


Coverage
--------

In order to get the coverage:

```bash
$ coverage run --source='.' -m py.test
$ coverage html
$ cd htmlcov/
$ open index.html # with your fav browser
```

Linting & pep8
--------------

In order to check if everything is ok according to pep8 rules, you can use
[flake8] (https://pypi.python.org/pypi/flake8) from the project root:
	
    $ flake8 loki
