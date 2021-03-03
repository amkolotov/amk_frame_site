from views import CourseListView, CategoryListView, StudentCreateView, StudentListView, CategoryCreateView, \
    AddStudentView, CourseCreateView

urlpatterns = {
    '/': CourseListView(),
    '/category-list/': CategoryListView(),
    '/create-course/': CourseCreateView(),
    '/create-category/': CategoryCreateView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentView(),
    '/student-list/': StudentListView(),
}