from .base import *

import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default="postgres://colracljnolrlk:ab5071cce04686e8345d3dd0d83af53b8ca8e010377fd65053ccbf92c2cc1c84@ec2-52-54-140-137.compute-1.amazonaws.com:5432/d9b2hui0trp3gg",
        conn_max_age = 600,
        conn_health_checks = True,
        ssl_require = True,
    ),
}
