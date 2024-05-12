from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from api import models
from api.utils.hook import HookSerializer
from api.utils.pagination import CustomPagination

class UserSerializer(HookSerializer, serializers.ModelSerializer):
    class Meta:
        model = models.User
        # fields = [
        #     "_id", "avatar", "bio", "birthday", "create_at", "email", "gender",
        #     "job", "nickname", "password", "phone", "update_at", "username"
        # ]
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "password": { "write_only": True },
            "update_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

    def hk_gender(self, obj):
        return obj.get_gender_display()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

class TopicSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tags = TagSerializer(many=True)
    class Meta:
        model = models.Topic
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "update_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

def fetch_topics(request, username = None, favor = False):
    if username is not None:
        user = models.User.objects.get(username=username)
    else:
        user = request.user

    favorites = models.User.objects.get(_id=user._id).favorite.all()
    favorite_ids = [f._id for f in favorites]
    print("User's favorite topics id: {}\n".format(favorite_ids))

    if favor:
        topics_all = models.Topic.objects.filter(_id__in=favorite_ids).order_by("-create_at")
        total = len(favorite_ids)
    else:
        topics_all = models.Topic.objects.filter(user=user._id).order_by("-create_at")
        total = models.Topic.objects.filter(user=user._id).count()

    page = CustomPagination()
    topics = page.paginate_queryset(topics_all, request)
    ser_topics = TopicSerializer(topics, many=True)
    ser_user = UserSerializer(user)
    return (page, ser_topics.data, total, ser_user.data)

class TopicListView(APIView):
    """
    GET:
    Return a list of all the topics.

    POST:
    Create a new topic instance.
    """
    def get(self, request, *args, **kwargs):
        topics_all = models.Topic.objects.all().order_by("-create_at")
        total = models.Topic.objects.count()
        page = CustomPagination()
        topics = page.paginate_queryset(topics_all, request)
        ser = TopicSerializer(topics, many=True)
        return page.get_paginated_response(ser.data, msg="Topics query succeed.", total=total)

    def post(self, request, *args, **kwargs):
        ser = TopicSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            res = { "data": ser.data, "msg": "Topic create succeed." }
            return Response(res)
        else:
            res = { "data": ser.errors, "msg": "Topic create failed." }
            return Response(res)

class UserTopicListView(APIView):
    """
    GET:
    Return a list of user's own topics.
    """
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        (page, data, total, user) = fetch_topics(request, username)
        return page.get_paginated_response(data, msg="User topics query succeed.", total=total, user=user)

class FavoriteTopicListView(APIView):
    """
    GET:
    Return a list of user's favorite topics.
    """
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        (page, data, total, user) = fetch_topics(request, username, True)
        return page.get_paginated_response(data, msg="User topics query succeed.", total=total, user=user)

class TopicDetailView(APIView):
    """
    GET:
    Return a single topic instance.

    PUT:
    Update a topic instance.

    DELETE:
    Delete a topic instance.
    """
    def get(self, request, *args, **kwargs):
        _id = kwargs.get("_id")
        topic = models.Topic.objects.get(_id=_id)
        ser = TopicSerializer(topic)
        res = { "data": ser.data, "msg": "Topic query succeed." }
        return Response(res)

    def put(self, request, *args, **kwargs):
        _id = kwargs.get("_id")
        topic = models.Topic.objects.get(_id=_id)
        ser = TopicSerializer(topic, data=request.data)
        if ser.is_valid():
            ser.save()
            res = { "data": ser.data, "msg": "Topic update succeed." }
            return Response(res)
        else:
            res = { "data": ser.errors, "msg": "Topic update failed." }
            return Response(ser.errors)

    def delete(self, request, *args, **kwargs):
        _id = kwargs.get("_id")
        topic = models.Topic.objects.get(_id=_id)
        topic.delete()
        res = { "data": None, "msg": "Topic delete succeed." }
        return Response(res)

class UserListView(APIView):
    """
    GET:
    Return a list of all the users.

    POST:
    Create a new user instance.
    """
    def get(self, request, *args, **kwargs):
        users_all = models.User.objects.all().order_by("-create_at")
        total = models.User.objects.count()
        page = CustomPagination()
        users = page.paginate_queryset(users_all, request)
        ser = UserSerializer(users, many=True)
        return page.get_paginated_response(ser.data, msg="Users query succeed.", total=total)

    def post(self, request, *args, **kwargs):
        ser = UserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            res = { "data": ser.data, "msg": "User create succeed." }
            return Response(res)
        else:
            res = { "data": ser.errors, "msg": "User create failed." }
            return Response(res)

class UserDetailView(APIView):
    """
    GET:
    Return a single user instance.

    PUT:
    Update a user instance.

    DELETE:
    Delete a user instance.
    """
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        user = models.User.objects.get(username=username)
        ser = UserSerializer(user)
        res = { "data": ser.data, "msg": "User query succeed." }
        return Response(res)

    def put(self, request, *args, **kwargs):
        username = kwargs.get("username")
        user = models.User.objects.get(username=username)
        ser = UserSerializer(user, data=request.data)
        if ser.is_valid():
            ser.save()
            res = { "data": ser.data, "msg": "User update succeed." }
            return Response(res)
        else:
            res = { "data": ser.errors, "msg": "User update failed." }
            return Response(res)

    def delete(self, request, *args, **kwargs):
        username = kwargs.get("username")
        user = models.User.objects.get(username=username)
        user.delete()
        res = { "data": None, "msg": "User delete succeed." }
        return Response(res)

