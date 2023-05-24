from django.urls import path
from web.views import ChangePasswordView

from . import views
app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('profile', views.profile, name='profile'),
    path('change_password', ChangePasswordView.as_view(), name='change_password'),
]