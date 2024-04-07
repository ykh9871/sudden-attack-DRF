from django.urls import path
from .views import (
    CategoryListView,
    BoardListView,
    BoardCreateView,
    BoardDetailView,
    BoardCommentListView,
    BoardCommentCreateView,
    BoardCommentDetailView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("groups/<int:group_id>/boards/", BoardListView.as_view(), name="board-list"),
    path(
        "groups/<int:group_id>/boards/create/",
        BoardCreateView.as_view(),
        name="board-create",
    ),
    path("boards/<int:pk>/", BoardDetailView.as_view(), name="board-detail"),
    path(
        "boards/<int:board_id>/comments/",
        BoardCommentListView.as_view(),
        name="board-comment-list",
    ),
    path(
        "boards/<int:board_id>/comments/create/",
        BoardCommentCreateView.as_view(),
        name="board-comment-create",
    ),
    path(
        "comments/<int:pk>/",
        BoardCommentDetailView.as_view(),
        name="board-comment-detail",
    ),
]
