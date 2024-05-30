from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from api.models import Tag, Topic, User
from api.serializers import UserSerializer, TagSerializer, TopicReadSerializer, TopicWriteSerializer
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
        user = User.objects.get(username=username)
    else:
        user = request.user

    favorites = User.objects.get(_id=user._id).favorite.all()
    favorite_ids = [f._id for f in favorites]
    print("User's favorite topics id: {}\n".format(favorite_ids))

    if favor:
        topics_all = Topic.objects.filter(_id__in=favorite_ids).order_by("-create_at")
        total = len(favorite_ids)
    else:
        topics_all = Topic.objects.filter(user=user._id).order_by("-create_at")
        total = Topic.objects.filter(user=user._id).count()

    page = CustomPagination()
    topics = page.paginate_queryset(topics_all, request)
    ser_topics = TopicReadSerializer(topics, many=True)
    ser_user = UserSerializer(user)
    return (page, ser_topics.data, total, ser_user.data)

class TagViewSet(ViewSet):
    """
    A simple ViewSet for tags.

    GET list:
    Return a list of all the tags.

    GET retrieve:
    Return a tag instance.

    POST create:
    Create a new tag instance.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def list(self, request):
        tags = Tag.objects.all().order_by("-create_at")
        total = Tag.objects.count()
        ser = TagSerializer(tags, many=True)
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "Tags query succeed.", "total": total })

class TopicViewSet(ViewSet):
    """
    A simple ViewSet for topics.

    GET list:
    Return a list of all the topics.

    GET retrieve:
    Return a topic instance.

    POST create:
    Create a new topic instance.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def list(self, request):
        topics_all = Topic.objects.all().order_by("-create_at")
        total = Topic.objects.count()
        page = CustomPagination()
        topics = page.paginate_queryset(topics_all, request)
        ser = TopicReadSerializer(topics, many=True)
        return page.get_paginated_response(ser.data, msg="Topics query succeed.", total=total)

    def retrieve(self, request, pk=None):
        topic = Topic.objects.get(pk=pk)
        ser = TopicReadSerializer(topic)
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "Topic query succeed." })

    def create(self, request):
        tags_str = request.data.pop("tags")
        tags = []
        for tag_str in tags_str:
            tag, _ = Tag.objects.get_or_create(tag=tag_str)
            tags.append(tag._id)
        request.data["tags"] = tags

        ser = TopicWriteSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response({ "code": status.HTTP_201_CREATED, "data": ser.data, "msg": "Topic create succeed." })
        else:
            return Response({ "code": status.HTTP_400_BAD_REQUEST, "error": ser.errors, "msg": "Topic create failed." })

class UserViewSet(ViewSet):
    """
    A simple ViewSet for users.

    GET list:
    Return a list of all the users.

    GET retrieve:
    Return a user instance.

    POST create:
    Create a new user instance.
    """
    def list(self, request):
        users_all = User.objects.all().order_by("-create_at")
        total = User.objects.count()
        page = CustomPagination()
        users = page.paginate_queryset(users_all, request)
        ser = UserSerializer(users, many=True)
        return page.get_paginated_response(ser.data, msg="Users query succeed.", total=total)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get("username")
        user = User.objects.get(username=username)
        ser = UserSerializer(user)
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "User info query succeed." })
