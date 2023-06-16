from django.urls import path, include
from . import views

urlpatterns = [
    path("login/",views.Login.as_view()),
    path("logout/",views.Logout.as_view()),
    path('reset/', views.ResetPasswordRequest.as_view()),
    path('reset/confirm/', views.ResetPassword.as_view()),
]