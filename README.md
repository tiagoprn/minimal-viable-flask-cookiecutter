# minimal viable flask cookiecutter

This project is a minimalistic flask template that can be used as a base to develop simple APIs on the Flask Framework, with swagger documentation integrated.

## You already have a cookiecutter pretty similar. So, Why this project?

It was derived from [a development branch of my old cookiecutter](https://github.com/tiagoprn/minimal_flask_app_cookiecutter/tree/refactored-extensions), which was being modernized to current packages' versions, and having celery and db support being refactored to the modular factory/blueprints/extensions architecture recommended on Flask's official site. The celery and db support has been removed from this project to keep the footprint really minimal, to serve as a less bloated starting point.

This project will on a future time frame also feed [its' original cookiecutter](https://github.com/tiagoprn/minimal_flask_app_cookiecutter) to automate this setup, providing optional celery and db support.

## Features

- A Makefile to wrap the most common operations and ease project management and , with commands to run the development server, the shell, etc...

- python 3.9

- flask 2.0

- flasgger (swagger wrapper) as documentation for the API, using doctrings on the API endpoints to write the documentation.

- gunicorn configured to run the project in the production environment.

- pylint as the linter, black as the code formatter, isort to fix import order

- pytest tests, with some plugins to ease presentation.

- environment variables for configuration.

- coverage report.

- docker/podman image generation (properly tagged)

- Sample endpoints working


## How to use this cookiecutter

- Install cookiecutter on your distribution (e.g. Ubuntu):

`$ sudo apt install cookiecutter`

- If you want to clone this repository locally to run the cookiecutter also locally:

```
$ mkdir -p ~/cookiecutters
$ cd ~/cookiecutters
$ git clone  https://github.com/tiagoprn/minimal-viable-flask-cookiecutter
```

- Enter the folder where your want to create your project locally:

```
cd ~/projects/
```

- Run the cookiecutter from the local copy:

`$ cookiecutter ~/cookiecutters/minimal-viable-flask-cookiecutter

... or directly from github (recommended):

`$ cookiecutter gh:tiagoprn/minimal-viable-flask-cookiecutter

It will ask some questions with sane defaults, and then will generate a folder with the value you
indicated for `project_slug`. Congratulations, this is your new minimal flask project! :)

- Enter the project directory:

`$ cd ~/projects/your-project_slug`

- Create a virtualenv to the project. If you're using pyenv:

```
$ pyenv virtualenv 3.9.1 your-project_slug
$ pyenv activate your-project_slug
```

- Install the development requirements:

`$ make requirements`

- Run the make command to create the sample configuration file:

```
$ make init-env
```

- Create a local git repository to bootstrap version control:

```
$ git init
$ git add .
$ git commit -m 'Boostrapping project.'
```

- Run the formatter, linter and tests:

```
$ make style && make style-check
$ make lint
$ make test
```

- Start the development server:

`$ make runserver-dev`

... or start the production server (gunicorn):

`$ make runserver`


