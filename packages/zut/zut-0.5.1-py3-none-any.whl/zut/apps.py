"""
Indicate Django application directory. Allows zut to be added in INSTALLED_APP with simple name:

    INSTALLED_APP = [
        ...
        'zut',
        ...
    ]
"""
from django.apps import AppConfig
from pathlib import Path

class ZutAppConfig(AppConfig):
    name = "zut"
    path = str(Path(__file__).parent.joinpath("django"))
