from auth import views
from django.urls import re_path


urlpatterns = [
    re_path('login', views.AuthView.as_view()),
    re_path('registration', views.RegistrationView.as_view()),
]