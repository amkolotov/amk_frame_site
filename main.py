import sys

sys.path.append('../')
from amk_framework.core import Application, LogApplication, FakeApplication


def my_controller(request):
    request['my_key'] = 'key'


controllers = [
    my_controller
]

app = Application(controllers)
# app = LogApplication(controllers)
# app = FakeApplication(controllers)

import views

from urls import urlpatterns

app.urls.update(urlpatterns)

# Запуск:
# gunicorn main:app
