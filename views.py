import sys

sys.path.append('../')
from amk_framework.templates import render


def index(request):
    key = request.get('my_key', None)
    return '200 OK', render('index.html', key=key)

def about(request):
    return '200 OK', render('about.html')
