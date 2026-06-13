from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Student
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/submissions/', views.my_submissions, name='my_submissions'),
    path('student/delete/<int:pk>/', views.delete_achievement, name='delete_achievement'),

    # Faculty
    path('faculty/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/review/<int:pk>/', views.review_achievement, name='review_achievement'),

    # Admin
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.manage_users, name='manage_users'),
    path('admin-panel/users/<int:pk>/toggle/', views.toggle_user_active, name='toggle_user_active'),

    # Shared
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
