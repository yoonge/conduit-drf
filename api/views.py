from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from api import models
from api.serializers import UserSerializer, TagSerializer, TopicSerializer
from api.utils.pagination import CustomPagination

@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def api_root(request, format=None):
    """
    API root.
    """
    return Response({
        "tags": reverse("tag-list", request=request, format=format),
        "topics": reverse("topic-list", request=request, format=format),
        "users": reverse("user-list", request=request, format=format),
    })

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

class TagViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving tags.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def list(self, request, *args, **kwargs):
        tags = models.Tag.objects.all().order_by("-create_at")
        total = models.Tag.objects.count()
        ser = TagSerializer(tags, many=True)
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "Tags query succeed.", "total": total })

class TopicViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving topics.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def list(self, request):
        topics_all = models.Topic.objects.all().order_by("-create_at")
        total = models.Topic.objects.count()
        page = CustomPagination()
        topics = page.paginate_queryset(topics_all, request)
        ser = TopicSerializer(topics, many=True)
        return page.get_paginated_response(ser.data, msg="Topics query succeed.", total=total)

    def retrieve(self, request, pk=None):
        topic = models.Topic.objects.get(pk=pk)
        ser = TopicSerializer(topic)
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "Topic query succeed." })

class UserViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    def list(self, request):
        users_all = models.User.objects.all().order_by("-create_at")
        total = models.User.objects.count()
        page = CustomPagination()
        users = page.paginate_queryset(users_all, request)
        ser = UserSerializer(users, many=True)
        return page.get_paginated_response(ser.data, msg="Users query succeed.", total=total)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get("username")
        user = models.User.objects.get(username=username)
        ser = UserSerializer(user)
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "User info query succeed." })
