import sys

from mappers import MapperRegistry
from models import TrainingSite, BaseSerializer
from main import app

sys.path.append('../')
from amk_framework.templates import render
from amk_framework.logging_mod import Logger, debug
from amk_framework.cbv import ListView, CreateView
from amk_framework.common.unitofwork import UnitOfWork

site = TrainingSite()
logger = Logger('main')

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


class CourseListView(ListView):
    queryset = site.courses
    template_name = 'index.html'

# @app.add_route('/')
# def courses_list(request):
#     logger.log('Вывод списка курсов')
#     return '200 OK', render('index.html', objects_list=site.courses)


class CategoryListView(ListView):
    queryset = site.categories
    template_name = 'category_list.html'

# @app.add_route('/category-list/')
# def category_list(request):
#     logger.log('Вывод списка категорий')
#     return '200 OK', render('category_list.html', objects_list=site.categories)


class CourseCreateView(CreateView):
    template_name = 'create_course.html'
    queryset = site.categories


    def create_object(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', name, category)
            site.courses.append(course)

# @app.add_route('/create-course/')
# def create_course(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#         category_id = data.get('category_id')
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#             course = site.create_course('record', name, category)
#             site.courses.append(course)
#
#     categories = site.categories
#
#     return '200 OK', render('create_course.html', objects_list=categories)


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'
    queryset = site.categories

    def create_object(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)


# @app.add_route('/create-category/')
# @debug
# def create_category(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#         category_id = data.get('category_id')
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#
#     categories = site.categories
#
#     return '200 OK', render('create_category.html', objects_list=categories)


class StudentListView(ListView):
    # queryset = site.students
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('student')
        return mapper.all()


# @app.add_route('/student-list/')
# def student_list(request):
#     print(site.students[0].courses[0].name)
#     return '200 OK', render('student_list.html', objects_list=site.students)


class StudentCreateView(CreateView):
    template_name = 'create_student.html'
    queryset = site.students

    def create_object(self, data: dict):
        name = data['name']
        student = site.create_user('student', name)
        site.students.append(student)
        student.mark_new()
        UnitOfWork.get_current().commit()

# @app.add_route('/create-student/')
# def create_student(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#         student = site.create_user('student', name)
#         site.students.append(student)
#         return '200 OK', render('student_list.html', objects_list=site.students)
#
#     return '200 OK', render('create_student.html')


class AddStudentView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_object(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)


# @app.add_route('/add-student/')
# def add_student(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         for course in site.courses:
#             if course.name == data['course_name']:
#                 add_course = course
#                 break
#         for student in site.students:
#             if student.name == data['student_name']:
#                 student.courses.append(add_course)
#                 return '200 OK', render('student_list.html', objects_list=site.students)
#
#     return '200 OK', render('add_student.html', students=site.students, courses=site.courses)



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


@app.add_route('/contact/')
def contact(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Пришло сообщение от {email} с заголовком "{title}" и текстом "{text}"')
    return '200 OK', render('contact.html')


@app.add_route('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.courses).save()

