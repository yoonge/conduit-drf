from django.urls import path, re_path
from api import views

urlpatterns = [
    path("", views.TopicListView.as_view()),
    re_path(r"^/topic/(?P<_id>\d+)$", views.TopicDetailView.as_view()),
    path("/user", views.UserListView.as_view()),
    path("/user/<str:username>", views.UserDetailView.as_view()),
]
