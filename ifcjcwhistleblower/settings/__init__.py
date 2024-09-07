# used the following link for setting up multiple environments
# https://nsikakimoh.com/blog/use-multiple-settings-files-in-django
try:
  from .development import *
except:
  from .production import *
