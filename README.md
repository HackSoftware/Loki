# Loki

Loki is son of Odin. That project stores all the data of HackBulgaria.
It takes care of all the courses and HackFMI! It is developed by HackBulgaria Software team!

Local development setup
-----------------------

The project is using:

-   Python 3.5+
-   Django 1.8+

In order to setup it, there are the following steps:

-   Install python requirements:

<!-- -->

    $ pip install -r requirements.txt

-   Setup Postgres

<!-- -->

    $ sudo -u postgres createuser your_postgres_username
    $ sudo -u postgres createdb -O your_postgres_username hack_training

-   Setup local settings

<!-- -->

    $ cp example_local_settings.py local_settings.py

    Fill up the you local settings

-   Run migrations

<!-- -->

    $ python manage.py makemigrations
    $ python manage.py migrate

-   Run server

<!-- -->

    $ python manage.py runserver

-   Install npm

<!-- -->

    $ sudo apt-get install npm
    & sudo apt-get install nodejs-legacy

-   Install bower

<!-- -->

    $ sudo npm install -g bower



Celery
------

This project is using Celery for async tasks such as email sending and working with Grader API.

In order to run Celery, you are going to need **RabbitMQ Server**

The following variables are taking care of everything, you just have to add it in our local_settings file:

    BROKER_URL="amqp://guest:guest@localhost//"

Afer this, you can run Celery:

    $ celery -A loki worker -B

Grader
------

We use [Grader](https://github.com/HackBulgaria/HackTester) in order to test the solution sent by student. In order to use the Grader API

you need to set values to the following variables in the local_settings file :

    GRADER_ADDRESS = "grader-address"
    GRADER_API_KEY = "grader-api-key"
    GRADER_API_SECRET = "your-grader-api-secret-key"



Email Confirmations  -------------------

In order to send confirmation emails, we must set the following variables in the local_settings file:
EMAIL_USE_TLS = 'True/False'
EMAIL_HOST = 'host'
EMAIL_PORT = 'port'
EMAIL_HOST_USER = 'host_user'
EMAIL_HOST_PASSWORD = 'password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


The email backend is controlled by the
`EMAIL_BACKEND` variable, which you can set up in the settings file 


Basic Commands
--------------

### Setting Up Your Users

-   To create an **superuser account**, use this command:

        $ python manage.py createsuperuser


- 
### Tests

#### Running tests

After you have installed all of the requirements, you can run the tests with:

    $ python manage.py test


Linting & pep8
--------------

In order to check if everything is ok according to pep8 rules, you can use
[flake8] (https://pypi.python.org/pypi/flake8) from the project root:
		
	$ flake8
