# ⌨️ Conduit DRF(Django REST Framework)

![version](https://img.shields.io/badge/version-0.2.0-green) [![license](https://img.shields.io/badge/license-MIT-blue)](./LICENSE) ![django](https://img.shields.io/badge/django-4.2.11-113229) ![python](https://img.shields.io/badge/python-%3E%3D3.12.3-3776ab) ![mysql](https://img.shields.io/badge/mysql-8.3.0-02758f) ![pdm](https://img.shields.io/badge/pdm-2.15.1-ac75d7)


## 💡 Introduction

Realworld: "The mother of all demo apps" — Exemplary back-end Medium.com clone (called [Conduit](https://github.com/yoonge/conduit-drf)) in Python, built with Django + DRF + MySQL + MySQLClient + PDM.

![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)
![Django Badge](https://img.shields.io/badge/django-4?logo=django&labelColor=%23092E20&color=white)


## 🔰 Getting Started

```sh
$ git clone https://github.com/yoonge/conduit-drf.git

$ cd conduit-django-ssr

# Activate the virtual environment
$ source ./.venv/bin/activate   # MacOS
$ ./.venv/Scripts/activate  # Windows

$ pdm install

$ pdm start

# open anthoer terminal
$ source ./.venv/bin/activate

$ pdm makemigrations

$ pdm migrate

$ pdm createsuperuser
```


<!-- ## 📁 Index -->


<!-- ## ⚡ Features -->


<!-- ## 📌 TODO -->


## 📄 License

Conduit DRF is [MIT-licensed](./LICENSE).


<!-- ## 🔗 Links -->


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

$ pdm add djangorestframework, djangorestframework-simplejwt, mysqlclient
```

## 🛠️ `settings.py`

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


NON_FIELD_ERRORS_KEY = "custom_errors"


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
