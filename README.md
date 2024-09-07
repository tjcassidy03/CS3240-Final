[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/qgEWmaMc)
# IFC JC Whistle Blower Application

__Name__: Lowell Jones, Julian Donald, Thomas Cassidy, Xiaotian Gu, Evan Yuan

__Computing ID:__ cqc2ch, jed5gpx, gvk9wu, zrj7dx, hdn6fv

## Dependencies

This project uses a few different dependencies to run. Assuming you have a virtual environment set up for python 3.9+, you can run the following command to install them all.

```sh
python -m pip install -r requirements.txt
```

## Additional Setup

A file for setting up the variables for local development is required, but not in this repository as it's not meant to be deployed to Heroku. Instead, create the following file on your system locally:

```python
# ifcjcwhistleblower/settings/development.py
from .base import *

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}
```
