# ⌨️ Conduit Django REST Framework

Realworld: "The mother of all demo apps" — Exemplary back-end Medium.com clone (called [Conduit](https://github.com/yoonge/conduit-drf)), built with Django + DRF + MySQL + MySQLClient + PDM.

![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)
![Django Badge](https://img.shields.io/badge/django-4?logo=django&labelColor=%23092E20&color=white)

## 💡 Use this template

```sh
$ pdm init django
```

Or create a new project at the given path:

```sh
$ pdm init -p django_project django
```

Visit https://localhost:8000 to see the welcome page.

## 🔰 Development

Create a new app:

```sh
$ pdm run manage.py startapp <app_name>
```

Migrate DB:

```sh
$ pdm migrate
```

Start development server:

```sh
$ pdm start
```

Call other `manage.py` commands:

```sh
$ pdm run manage.py <command> [options]
```

## 📄 License

This project is licensed under the terms of the MIT license.


----


## 🏗️ Scaffold

```sh
$ pip install pdm

$ mkdir conduit-drf && cd conduit-drf

$ pdm init django

 # Activate the virtual environment
$ source ./.venv/bin/activate   # MacOS
$ ./.venv/Scripts/activate  # Windows

$ py manage.py startapp api

$ pdm add djangorestframework
```

### `settings.py`

```py
# Application definition

INSTALLED_APPS = [
    # "django.contrib.admin",
    # "django.contrib.auth",
    # "django.contrib.contenttypes",
    # "django.contrib.sessions",
    # "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    # "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conduit_drf.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                # "django.contrib.auth.context_processors.auth",
                # "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ...


# LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"


# ...


AUTH_USER_MODEL = "api.User"


LOGIN_REDIRECT_URL = "/api/"
LOGOUT_REDIRECT_URL = "/api/"


# APPEND_SLASH = False
# SILENCED_SYSTEM_CHECKS = ['urls.W002']


# REST framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "api.utils.pagination.CustomPagination",
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "UNAUTHENTICATED_USER": None,
}


# DRF Simple JWT

SIMPLE_JWT = {
    "USER_ID_FIELD": "_id",
    "TOKEN_OBTAIN_SERIALIZER": "api.serializers.MyTokenObtainPairSerializer",
}
```
