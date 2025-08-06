from django.urls import path

from app_boards import views as app_board_views

urlpatterns = [
    path(
        "create/",
        app_board_views.CreateBoardAPIView.as_view(),
        name='create-board'
    ),
    path(
        "list/",
        app_board_views.ListBoardsAPIView.as_view(),
        name='list-board'
    ),
    path(
        "close/",
        app_board_views.CloseBoardAPIView.as_view(),
        name='close-board'
    ),
    path(
        "export/",
        app_board_views.ExportBoardAPIView.as_view(),
        name='export-board'
    )
]

urlpatterns += [
    path(
        "tasks/create/",
        app_board_views.AddTaskAPIView.as_view(),
        name='create-task'
    ),
    path(
        "tasks/update-status/",
        app_board_views.UpdateTaskStatusAPIView.as_view(),
        name='update-task-status'
    ),
]
