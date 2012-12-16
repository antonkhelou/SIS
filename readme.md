Smart Image Serve
=================

Dependencies
------------
* Python 2.7
* Django 1.4
* PIL

Development
-----------

virtualenv should be used to manage dependencies

to install it: `sudo pip install virtualenv`

Create a virtual environment:

in your checked out directory, run

    virtualenv --no-site-packages sis_env

Install all the dependencies:

    source sis_env/bin/activate
    
    pip install -r requirements.txt

if you need to add a dependency, install it with pip then run

    pip freeze > requirements.txt

and commit the requirements file


Instructions
------------

* Check out the source with `git clone git@github.com:antonkhelou/SIS.git smart_img_serve`
* `cd` into the smart_img_serve directory
* `source sis_env/bin/activate` to setup the virtualenv
* `python manage.py runserver`. Access the site at http://localhost:8000


Project layout
-------------

* `db.sqlite` - for development only. not tracked by git. created upon running `python manage.py syncdb`
* `data.pdf` - some pixelation data results.
* `manage.py` - comes with Django. Not modified.
* `readme.md`
* `sis/`
    * `settings.py` - the project-wide settings. should not need to be changed.
    * `templates/` - all the template files will go under here. there will be a directory for each app.
    * `urls.py` - includes all the urls.py files for each app (e.g. `correction/urls.py`) and maps the base url to the `home` view defined in `views.py`.
    * `views.py` - includes all views which are mapped with the urls patterns specifies in `views.py`.