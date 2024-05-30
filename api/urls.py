from django.urls import path, re_path
from api import views

urlpatterns = [
    path("", views.api_root),
    path("tags/", views.TagViewSet.as_view({ "get": "list" }), name="tag-list"),
    path("topics/", views.TopicViewSet.as_view({ "get": "list", "post": "create" }), name="topic-list"),
    re_path(r"^topic/(?P<pk>\d+)/$", views.TopicViewSet.as_view({ "get": "retrieve" }), name="topic-detail"),
    path("users/", views.UserViewSet.as_view({ "get": "list" }), name="user-list"),
    path("user/<str:username>/", views.UserViewSet.as_view({ "get": "retrieve" }), name="user-detail"),
    # path("", views.TopicListView.as_view()),
    # path("my-topics/", views.UserTopicListView.as_view()),
    # path("my-favorites/", views.FavoriteTopicListView.as_view()),
    # path("profile/<str:username>/", views.UserTopicListView.as_view()),
    # path("profile/<str:username>/favorites/", views.FavoriteTopicListView.as_view()),
    # re_path(r"^topic/(?P<_id>\d+)/$", views.TopicDetailView.as_view()),
    # path("user/", views.UserListView.as_view()),
    # path("user/<str:username>/", views.UserDetailView.as_view()),
    # path("settings/", views.UserSettingsView.as_view()),
]
