import sys

from models import TrainingSite
from main import app

sys.path.append('../')
from amk_framework.templates import render
from amk_framework.logging_mod import Logger, debug

site = TrainingSite()
logger = Logger('main')


@app.add_route('/')
def index(request):
    logger.log('Вывод списка курсов')
    return '200 OK', render('index.html', objects_list=site.courses)


@app.add_route('/category-list/')
def category_list(request):
    logger.log('Вывод списка категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)


@app.add_route('/contact/')
def contact(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Пришло сообщение от {email} с заголовком "{title}" и текстом "{text}"')
    return '200 OK', render('contact.html')


@app.add_route('/create-course/')
def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)

    categories = site.categories

    return '200 OK', render('create_course.html', objects_list=categories)


@app.add_route('/create-category/')
@debug
def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)

    categories = site.categories

    return '200 OK', render('create_category.html', objects_list=categories)


@app.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']

    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('index.html', objects_list=site.courses)


