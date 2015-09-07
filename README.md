# Yogo

## What is Yogo?

Yogo is a super simple way to create polls online.

## What does Yogo run on?

Bezzist is powered by several technologies.

API Server:
- Python
- [Django](https://www.djangoproject.com/) (and many libraries)
- [Restless](http://restless.readthedocs.org/en/latest/)
- [Gunicorn](http://gunicorn.org/)

Database:
- [Postgres](http://www.postgresql.org/)
- Psycopg2 (Python-to-Postgres ORM)

Frontend:
- [React](http://facebook.github.io/react/)
- [Flux](http://facebook.github.io/flux/)
- Browserify + UglifyJS2
- Node + NPM

### Setting Up Dev Environment

For this section, I will assume that you are running on LINUX, OSX, or putty.

First, **download, install, and start Postgres**. It can be downloaded from the
[Postgres official website](http://www.postgresql.org). If you have a Mac, I
highly suggest the [postgres.app application](http://www.postgresql.org/download/macosx/)
-- it's super easy to set up. Follow the instructions on the website to
install and start Postgres.

Second, **install [Virtualenv](http://virtualenv.readthedocs.org/)**, if you don't
already have it. Why it's always a good idea to have an isolated environment
is outlined in that web page.

Third, once Virtualenv is installed, **create a virtual environment** in the directory
where you want to keep Yogo.
```
$ virtualenv yogo
```

Fourth, navigate to the newly created virtual environment ``yogo`` and activate
your virtual environment. Once that's done, **clone the Yogo repository**.
```
$ cd yogo && source bin/activate
$ git clone git@github.com:suchanlee/yogo.git
```

Fifth, navigate to the cloned repository directory. You now need to **download all
Python dependencies** that Yogo uses. These are all stored in ``requirements.txt``.
They can easily be downloaded by running the command:
```
$ pip install -r requirements.txt
```

Sixth, navigate to the ``static`` directory which should be located in
``<yogo_root_dir>/yogo/yogo/static``. You will now **download
all Javascript dependencies**. *Make sure that you have NPM and Node.js
installed*. If you don't, you can find out how to install it in the [official
Node.js website](https://nodejs.org/).

Seventh, in that directory, run:
```
$ npm install
$ npm start
```

This should compile the static files and start a watch process which
will watch the Javascript and CSS files and re-compile them if they are changed.
You can turn this process off with ``ctrl + c`` after the Javascript file builds
if you are not developing on the front end.

Eighth, **create a database**. You can create a database with the following
command (replace user and port as needed -- this should work for OSX):
```
$ createdb -U postgres -h localhost -p 5432 yogo
```

Ninth, **set up local settings**. Go to the ``settings/`` directory and
copy over ``local.py.template`` to ``local.py``. If you used the above
command to create your database, you should not need to change
anything in the file. But if you used a different user or have Postgres
running on a different port, open up ``local.py`` and edit the ``DATABASES``
field accordingly.

FINALLY, **start the Django server**. Go to the directory where ``manage.py``
file is and run
```
$ python manage.py runserver <PORT NUMBER>
```
