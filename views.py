import sys

sys.path.append('../')
from amk_framework.templates import render


def index(request):
    key = request.get('my_key', None)
    return '200 OK', render('index.html', key=key)


def about(request):
    return '200 OK', render('about.html')


def contact(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Пришло сообщение от {email} с заголовком "{title}" и текстом "{text}"')
    return '200 OK', render('contact.html')
