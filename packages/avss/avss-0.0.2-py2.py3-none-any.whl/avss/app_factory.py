from abc import ABC, abstractclassmethod

from avss.http import HttpRequest, HttpResponse
from avss.parser import HttpParser
from avss.settings import get_settings
import importlib
import sys


settings = get_settings()

class AppFactory:

    @classmethod
    def get_app(cls, http_request: HttpRequest):
        # TODO: Cache these on start.
        app = None
        for section in settings.sections():
            if section not in ['settings', 'default']:
                app_path = settings[section].get('path')
                app_name = settings[section].get('app')
                sys.path.append(app_path)
                app = importlib.import_module(app_name)
                app = getattr(app, 'main')
                print(app)

        if app is None:
            from avss.app import DefaultApp
            return DefaultApp

        return app

