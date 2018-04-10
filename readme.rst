Scipion Workflows
=================

Install
-------

To install this software, clone this repository and run::

  $ virtualenv --python /usr/bin/python3 .env
  $ . .env/bin/activate
  $ pip install -r requirements.txt
  $ python manage.py migrate


Running
-------

::

  $ python manage.py runserver

It will open a webserver listening at port 8000.
