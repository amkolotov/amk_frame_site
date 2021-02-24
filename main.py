import sys

sys.path.append('../')
from amk_framework.core import Application


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

import views

# Запуск:
# gunicorn main:app
