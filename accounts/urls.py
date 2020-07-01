from django.urls import path

from django.contrib.auth import views as auth_views
from . import views, forms

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('robots.txt', views.robots_txt, name='robots.txt'),
    path(
        'login/',
        views.LoginView.as_view(
            form_class=forms.AuthenticationForm,
            template_name='accounts/login.html',
        ),
        name='login'
    ),
    path(
        'logout/',
        views.LogoutView.as_view(template_name='accounts/logout.html'),
        name='logout'
    ),
    path('signup/', views.signup_page, name='signup'),
    path('switch/', auth_views.logout_then_login, name='switch'),
]
