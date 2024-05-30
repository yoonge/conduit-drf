from typing import Any, Dict
from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import Tag, Topic, User
from api.utils.hook import HookSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        default_data = super().validate(attrs)
        res = {
            "access": default_data["access"],
            "msg": "Login succeed.",
            "refresh": default_data["refresh"],
            "user": UserSerializer(self.user).data
        }
        return res

class UserSerializer(HookSerializer, ModelSerializer):
    class Meta:
        model = User
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

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

class TopicReadSerializer(ModelSerializer):
    tags = StringRelatedField(many=True)
    user = UserSerializer()

    class Meta:
        model = Topic
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "update_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

class TopicWriteSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ["content", "tags", "title", "user"]
