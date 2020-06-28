from django.urls import path

from . import views

# app_name = 'oj'
urlpatterns = [
    path('', views.index, name='problems'),
    path('robots.txt', views.robots_txt, name='robots.txt'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem'),
    path('problem/<int:problem_id>/submit/', views.submit, name='submit'),
    path('submission/<int:submission_id>/', views.submission_detail,
         name='submission'),
    path('submission/<int:submission_id>/json/', views.submission_json,
         name='submission.json'),
]
