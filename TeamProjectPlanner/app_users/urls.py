from django.urls import path

from app_users import views as app_users_view

urlpatterns = [
    path(
        "create/",
        app_users_view.CreateUserAPIView.as_view(),
        name="create-user"
    ),
    path(
        "list/",
        app_users_view.ListUsersAPIView.as_view(),
        name='list-user'
    ),
    path(
        "describe/",
        app_users_view.DescribeUserAPIView.as_view(),
        name='describe-user'
    ),
    path(
        "update/",
        app_users_view.UpdateUserAPIView.as_view(),
        name='update-user'
    ),
    path(
        "teams/",
        app_users_view.GetUserTeamsAPIView.as_view(),
        name='list-user-teams'
    ),
]
