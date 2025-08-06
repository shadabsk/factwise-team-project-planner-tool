from django.urls import path

from app_teams import views as app_teams_view

urlpatterns = [
    path(
        "create/",
        app_teams_view.CreateTeamAPIView.as_view(),
        name="create-team"
    ),
    path(
        "list/",
        app_teams_view.ListTeamsAPIView.as_view(),
        name='list-teams'
    ),
    path(
        "add-users/",
        app_teams_view.AddUsersToTeamAPIView.as_view(),
        name='add-user-to-team'
    ),
    path(
        "list-users/",
        app_teams_view.ListTeamUsersAPIView.as_view(),
        name='list-team-users'
    ),
    path(
        "describe/",
        app_teams_view.DescribeTeamAPIView.as_view(),
        name='describe-team'
    ),
    path(
        "update/",
        app_teams_view.UpdateTeamAPIView.as_view(),
        name='update-team'
    ),
    path(
        "remove-users/",
        app_teams_view.RemoveUsersFromTeamAPIView.as_view(),
        name='remove-user-from-team'
    )
]