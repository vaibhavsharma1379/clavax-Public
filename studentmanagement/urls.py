from django.urls import path
from .views import check_superuser, StudentUpdateForm,LoginForm,AddClass, StudentListCreateView, StudentRetrieveUpdateDestroyView,StudentLoginView,StudentProfileUpdateView,registerStudent_page,register,AddClassForm

urlpatterns = [
    path('student/registerPage/',registerStudent_page,name='student-register-page'),
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/loginview/',StudentLoginView, name='student-login'),
    path('student/profile/update/', StudentProfileUpdateView.as_view(), name='student_profile_update'),
    path('student/register/', register, name='api-register'),
    path('addclass/',AddClassForm , name='class-register'),
    path('addclassApi/',AddClass , name='api-class-register'),
    path('loginform/',LoginForm , name='api-login'),
    path('studentupdateform/',StudentUpdateForm , name='api-update'),
     path('check_superuser/', check_superuser, name='check_superuser'),
]
