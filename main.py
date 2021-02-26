import sys

sys.path.append('../')
from amk_framework.core import Application, LogApplication, FakeApplication


# urlpatterns = {
    # '/': views.index,
    # '/about/': views.about,
    # '/contact/': views.contact,
# }


def my_controller(request):
    request['my_key'] = 'key'


controllers = [
    my_controller
]

app = Application(controllers)
# app = LogApplication(controllers)
# app = FakeApplication(controllers)

import views

# Запуск:
# gunicorn main:app
