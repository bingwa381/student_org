from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('manage/students/', views.admin_students, name='admin_students'),
    path('manage/students/add/', views.admin_add_student, name='admin_add_student'),
    path('manage/students/assign/<int:student_id>/', views.assign_registration, name='assign_registration'),
    path('manage/approve/<int:student_id>/', views.approve_student, name='approve_student'),
    path('manage/delete/<int:student_id>/', views.delete_student, name='delete_student'),
]