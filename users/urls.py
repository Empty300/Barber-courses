from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (EmailVerificationView)

app_name = 'users'

urlpatterns = [
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    ]
