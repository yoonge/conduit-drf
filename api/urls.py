from django.urls import path, re_path
from api import views

urlpatterns = [
    path("", views.api_root),
    path("tags/", views.TagViewSet.as_view({ "get": "list" }), name="tag-list"),
    path("topics/", views.TopicViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="topic-list"),
    re_path(r"^topic/(?P<pk>\d+)/$", views.TopicViewSet.as_view({
        "delete": "destroy",
        "get": "retrieve",
        "put": "update",
    }), name="topic-detail"),
    path("users/", views.UserViewSet.as_view({
        "get": "list",
        "post": "create",
    }), name="user-list"),
    path("user/<str:username>/", views.UserViewSet.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    }), name="user-detail"),
    path("my-topics/", views.TopicViewSet.as_view({
        "get": "my_topics",
    }), name="my-own-topics"),
    path("my-favorites/", views.TopicViewSet.as_view({
        "get": "my_favorites",
    }), name="my-favorite-topics"),
    path("profile/<str:username>/", views.TopicViewSet.as_view({
        "get": "user_topics",
    }), name="user-own-topics"),
    path("profile/<str:username>/favorites/", views.TopicViewSet.as_view({
        "get": "user_favorites"
    }), name="user-favorite-topics"),
    # path("settings/", views.UserSettingsView.as_view()),
]
