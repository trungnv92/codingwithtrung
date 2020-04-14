from django.urls import path
from django.conf.urls import url
from account.api.views import registration_view, ChangePasswordView
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'
urlpatterns = [
    path('register/', registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
    url('change_password/', ChangePasswordView.as_view(), name='api_change_pass'),
]
