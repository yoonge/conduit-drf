from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from utils.hook import HookSerializer

class UserSerializer(HookSerializer, serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    # gender = serializers.CharField(source='get_gender_display', read_only=True)
    update_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = models.User
        # fields = ["_id", "avatar", "bio", "birthday", "create_at", "email", "gender", "job", "nickname", "password", "phone", "update_at", "username"]
        fields = "__all__"

    def hk_gender(self, obj):
        return obj.get_gender_display()

# Create your views here.
class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Hello, world!"})


class UserView(APIView):
    def get(self, request):
        users = models.User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
