from typing import Any, Dict
from rest_framework.serializers import CharField, ModelSerializer, StringRelatedField, \
    ValidationError
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
            "user": UserReadSerializer(self.user).data
        }
        return res

class UserReadSerializer(HookSerializer, ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "date_joined": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "last_login": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "password": { "write_only": True },
            "update_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

    def hk_gender(self, obj):
        return obj.get_gender_display()

class UserWriteSerializer(HookSerializer, ModelSerializer):
    confirm_password = CharField(max_length=128, read_only=True)

    class Meta:
        model = User
        fields = [
            "_id", "avatar", "bio", "birthday", "confirm_password", "create_at", "date_joined",
            "email", "favorite", "gender", "is_active", "is_staff", "job", "last_login",
            "nickname", "password", "phone", "update_at", "username"
        ]
        # fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "date_joined": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "is_staff": { "read_only": True },
            "last_login": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
            "password": { "write_only": True },
            "update_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already exists.")
        return value

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise ValidationError("Username already exists.")
        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        if "password" in attrs and "confirm_password" in attrs \
        and attrs["password"] != attrs["confirm_password"]:
            raise ValidationError("Passwords don't match.")
        return attrs

    def hk_gender(self, obj):
        return obj.get_gender_display()

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        extra_kwargs = {
            "create_at": { "format": "%Y-%m-%d %H:%M:%S", "read_only": True },
        }

class TopicReadSerializer(ModelSerializer):
    tags = StringRelatedField(many=True)
    user = UserReadSerializer()

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
