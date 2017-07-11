# Market_Manager_V2

The second version of the sales manager of the association Air-Eisti. It's a [Django](https://www.djangoproject.com/) (1.11.2) application using the css framework 
[bulma](http://bulma.io/) .

## Installation

### 1. virtualenv / virtualenvwrapper

You should already know what is virtualenv. So, simply create it for this project :

```$ mkvirtualenv Market_Manager_V2```

### 2. Download

Then you need to download the application :
```
$ cd /path/to/your/workspace
$ git clone https://github.com/AIR-EISTI/Market_Manager_V2.git
$ cd Market_Manager_V2
```

### 3. Requirements

The requirements.txt file contains all the libraries needed, to install them, simply launch :

```$ pip install -r requirements.txt```

### 4. Initialize the database

```
$ python manage.py makemigrations Snack
$ python manage.py migrate
```

## Tests
The tests can be launch as follow (`coverage` required) :

```
coverage run manage.py test Snack
```
or 

```
python manage.py test Snack
```

the verbosity level 2 or 3, `-v 2` or `-v 3`, can be added to have more detail.

Then launch ``` $ coverage report ``` to have a summary in percentage of the coverage.

``` $ coverage html ``` can be launch to have the html version of the coverage report, moreover
this shows what part of the code is not covered by the tests.


## License
This project follows the BSD license. See the [LICENSE](https://github.com/AIR-EISTI/Market_Manager_V2/blob/master/LICENSE)
for details.
