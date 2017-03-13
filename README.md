# Loki Project

  [![Build Status](https://travis-ci.org/HackSoftware/Loki.svg?branch=master)](https://travis-ci.org/HackSoftware/Loki)
  [![Coverage Status](https://coveralls.io/repos/github/HackSoftware/Loki/badge.svg?branch=master)](https://coveralls.io/github/HackSoftware/Loki?branch=master)

Loki is the **Learning Management System** used by [HackBulgaria](https://hackbulgaria.com) for their courses.

It stores the website & the LMS in one. APIs used by the [HackFMI app](https://github.com/HackSoftware/HackFMI-NG2) are also located here. The project is integrated with a [grader system](https://github.com/HackBulgaria/HackTester) for code checking & fast feedback loop for the students.

Developed by [HackSoft](http://hacksoft.io)

Local development setup
-----------------------

The project is using:

-   Python 3.5
-   Django 1.9

In order to setup it, there are the following steps:

-   Install python requirements:

<!-- -->

    $ pip install -r requirements/base.txt
    
-   Install Redis Server

<!-- -->

    $ sudo apt-get install redis server

-   Setup Postgres

<!-- -->

    $ sudo -u postgres createuser your_postgres_username
    $ sudo -u postgres createdb -O your_postgres_username your_postgres_database_name

-   Setup local environment variables


You can check [`config/settings`](config/settings) files for settings. Most of them are loaded as env variables.


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
