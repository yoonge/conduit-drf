from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api import models
from api.utils.hook import HookSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

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
