# Market_Manager_V2

The second version of the sales manager of the association Air-Eisti.
It's a [Django](https://www.djangoproject.com/) (1.11.2) application using the css framework [bulma](http://bulma.io/) .

## Installation

### 1. virtualenv / virtualenvwrapper

You should already know what is virtualenv. So, simply create it for this
project :

```$ mkvirtualenv Market_Manager_V2```

### 2. Download

Then you need to download the application :
```
$ cd /path/to/your/workspace
$ git clone https://github.com/AIR-EISTI/Market_Manager_V2.git
$ cd Market_Manager_V2
```

### 3. Requirements

The requirements.txt file contains all the libraries needed, to install them,
simply launch :

```$ pip install -r requirements.txt```

### 4. Initialize the database

```
$ python manage.py makemigrations Snack
$ python manage.py migrate
```

### 5. Create a admin user

```
$ python manage.py createsuperuser
```
or
```
$ python manage.py shell
>>> from django.contrib.auth.models import User
>>> user=User.objects.create_user('username', password='password')
>>> user.is_superuser=True
>>> user.is_staff=True
>>> user.save()
```

## Tests

### Launch test
The tests can be launch as follow (`coverage` required) :

```
coverage run manage.py test Snack
```
or 

```
python manage.py test Snack
```

the verbosity level 2 or 3, `-v 2` or `-v 3`, can be added to have more detail.

### Coverage Report

Then launch ``` $ coverage report ``` to have a summary in percentage of the
coverage.

``` $ coverage html ``` can be launch to have the html version of the coverage
report, moreover this shows what part of the code is not covered by the tests.

### Ignore files

If you want to ignored some file or folder, virtualenv folder for exemple,
create a ```.coveragerc```, and add :

```
[run]
omit = path/to/venv, manage.py, Snack/migrations/*
```

### Django_coverage_plugin

The plugin `django_coverage_plugin` allows the integration of the differents
templates during the coverage. Add this, in the `.coveragerc` file :

```
plugins =
    django_coverage_plugin
```

In order to use the plugin add `'debug': True` in the `settings.py` files
as follow :

```
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
            ],
            'debug': True,
        }
        ...
    }
]
```

## Run server

```
$ python manage.py runserver
```

## Deployment

Don't forget to pass all of the `debug` variable at `False`.

## Authors

- __Laurine Sorel__ - _Initial work_ - [DracarysBZH](https://github.com/DracarysBZH)
- __Tom__ - _Contributor_ - [Tjiho](https://github.com/Tjiho)

## License
This project follows the BSD 2-Clause License. See the
[LICENSE](https://github.com/AIR-EISTI/Market_Manager_V2/blob/development/LICENSE)
for details.

## Acknowledgments
- Inspired by the first version of Market_Manager create by [FunkySayu](https://github.com/FunkySayu) and [blQn](https://github.com/blqn)
- Readme inspired by [PurpleBooth/README-Template.md](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
