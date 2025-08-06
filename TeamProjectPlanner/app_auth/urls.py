from django.urls import path

from app_auth import views as app_auth_views

urlpatterns = [
    path("login/", app_auth_views.LoginAPIView.as_view(), name="login")
]
