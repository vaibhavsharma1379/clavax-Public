
from django.urls import path
from .views import StudentListCreateView, StudentRetrieveUpdateDestroyView,StudentLoginView,StudentProfileUpdateView

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDestroyView.as_view(), name='student-retrieve-update-destroy'),
    path('students/login/',StudentLoginView.as_view(), name='student-login'),
    path('student/profile/update/', StudentProfileUpdateView.as_view(), name='student_profile_update'),
]
