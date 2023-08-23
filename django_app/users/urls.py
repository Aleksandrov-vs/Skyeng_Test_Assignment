import django.contrib.auth.views
from django.contrib.auth import views as auth_views
from users.views import SingUpView
from django.urls import path

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(success_url='/'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(
            next_page='/account/login/'
        ),
        name='logout'
    ),
    path('sing-up/', SingUpView.as_view(), name='sing-up')
]
