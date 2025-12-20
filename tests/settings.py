DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

INSTALLED_APPS = ("vanilla_extract", "tests")

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

SECRET_KEY = "abcde12345"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

USE_TZ = False
