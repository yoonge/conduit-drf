from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet
from api.models import Tag, Topic, User
from api.serializers import TagSerializer, TopicReadSerializer, TopicWriteSerializer, \
    UserReadSerializer, UserWriteSerializer
from api.utils.pagination import CustomPagination

@api_view(["GET"])
@permission_classes((IsAuthenticatedOrReadOnly, ))
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
    ser_user = UserReadSerializer(user)
    return (page, ser_topics.data, total, ser_user.data)

class TagViewSet(ViewSet):
    """
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
    GET list:
    Return a list of all the topics.

    GET retrieve:
    Return a topic instance.

    POST create:
    Create a new topic instance and return it.

    PUT update:
    Update a topic instance and return it.

    DELETE destroy:
    Destroy a topic instance.
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
        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({ "code": status.HTTP_404_NOT_FOUND, "msg": "Topic not found." })

        ser = TopicReadSerializer(topic)
        return Response({
            "code": status.HTTP_200_OK,
            "data": ser.data,
            "msg": "Topic query succeed."
        })

    def create(self, request):
        tags_str = request.data.pop("tags")
        tags = []
        for tag_str in tags_str:
            tag, _ = Tag.objects.get_or_create(tag=tag_str.lower())
            tags.append(tag._id)
        request.data["tags"] = tags

        ser = TopicWriteSerializer(data=request.data)
        if not ser.is_valid():
            return Response({ "code": status.HTTP_400_BAD_REQUEST, "error": ser.errors, "msg": "Topic create failed." })

        ser.save()
        return Response({ "code": status.HTTP_201_CREATED, "data": ser.data, "msg": "Topic create succeed." })

    def update(self, request, pk=None):
        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({ "code": status.HTTP_404_NOT_FOUND, "msg": "Topic not found." })

        tags_str = request.data.pop("tags")
        tags = []
        for tag_str in tags_str:
            tag, _ = Tag.objects.get_or_create(tag=tag_str.lower())
            tags.append(tag._id)
        request.data["tags"] = tags

        ser = TopicWriteSerializer(topic, data=request.data)
        if not ser.is_valid():
            return Response({ "code": status.HTTP_400_BAD_REQUEST, "error": ser.errors, "msg": "Topic update failed." })

        ser.save()
        return Response({ "code": status.HTTP_200_OK, "data": ser.data, "msg": "Topic update succeed." })

    def destroy(self, request, pk=None):
        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({ "code": status.HTTP_404_NOT_FOUND, "msg": "Topic not found." })

        topic.delete()
        return Response({ "code": status.HTTP_204_NO_CONTENT, "msg": "Topic delete succeed." })

class UserViewSet(ViewSet):
    """
    GET list:
    Return a list of all the users.

    GET retrieve:
    Return a user instance.

    POST create:
    Create a new user instance and return it.

    PUT update:
    Update a user instance and return it.

    DELETE destroy:
    Destroy a user instance.
    """
    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAdminUser, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def list(self, request):
        users_all = User.objects.all().order_by("-create_at")
        total = User.objects.count()
        page = CustomPagination()
        users = page.paginate_queryset(users_all, request)
        ser = UserReadSerializer(users, many=True)
        return page.get_paginated_response(ser.data, msg="Users query succeed.", total=total)

    def retrieve(self, request, *args, **kwargs):
        try:
            username = kwargs.get("username")
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({ "code": status.HTTP_404_NOT_FOUND, "msg": "User not found." })

        ser = UserReadSerializer(user)
        return Response({
            "code": status.HTTP_200_OK,
            "data": ser.data,
            "msg": "User info query succeed."
        })

    def create(self, request):
        ser = UserWriteSerializer(data=request.data)
        if not ser.is_valid():
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "error": ser.errors,
                "msg": "User create failed."
            })

        instance = ser.save()
        return Response({
            "code": status.HTTP_201_CREATED,
            "data": UserReadSerializer(instance).data,
            "msg": "User create succeed."
        })

    def update(self, request, *args, **kwargs):
        try:
            username = kwargs.get("username")
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({ "code": status.HTTP_404_NOT_FOUND, "msg": "User not found." })

        ser = UserWriteSerializer(user, data=request.data, partial=True)
        if not ser.is_valid():
            return Response({
                "code": status.HTTP_400_BAD_REQUEST,
                "error": ser.errors,
                "msg": "User update failed."
            })

        instance = ser.save()
        return Response({
            "code": status.HTTP_200_OK,
            "data": UserReadSerializer(instance).data,
            "msg": "User update succeed."
        })

    def destroy(self, request, *args, **kwargs):
        try:
            username = kwargs.get("username")
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({ "code": status.HTTP_404_NOT_FOUND, "msg": "User not found." })

        user.delete()
        return Response({ "code": status.HTTP_204_NO_CONTENT, "msg": "User delete succeed." })
