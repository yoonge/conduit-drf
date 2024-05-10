from django.db import models

# Create your models here.
class User(models.Model):
    """ User Table """
    _id = models.AutoField("id", primary_key=True)
    avatar = models.CharField("avatar", max_length=256, default='/images/typescript.svg')
    bio = models.TextField("bio", default='')
    birthday = models.CharField("birthday", max_length=64, default='')
    create_at = models.DateTimeField("create at", auto_now_add=True)
    email = models.EmailField("e-mail", max_length=128, unique=True)
    job = models.CharField("job", max_length=256, default='')
    nickname = models.CharField("nickname", max_length=64, default='')
    password = models.CharField("password", max_length=128)
    phone = models.CharField("phone", max_length=11, default='')
    update_at = models.DateTimeField("update at", null=True, blank=True, auto_now=True)
    username = models.CharField("username", max_length=32, unique=True)

    # Cascade Delete
    # depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
    # Set NULL
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
    # avatar = models.ForeignKey(to="Avatar", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    gender_choices = (
        (-1, "Secret"),
        (0, "Female"),
        (1, "Male"),
    )
    gender = models.SmallIntegerField("gender", choices=gender_choices, default=-1)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    class Meta:
        indexes = [
            models.Index(fields=["username", "-create_at"]),
        ]
