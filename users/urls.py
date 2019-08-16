# 为应用程序users定义URL模型

from django.urls import include, path

from django.contrib.auth.views import LoginView

from . import views

app_name = 'users'

urlpatterns = [
    # login
    path(r'login/',LoginView.as_view(template_name='users/login.html'),name='login'),
    # logout
    path(r'logout/',views.logout_view,name='logout'),
    path(r'register/',views.register,name='register')
]