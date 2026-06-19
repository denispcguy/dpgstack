from pathlib import Path
import os
import platform
import shutil

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = bool(int(os.getenv("DJANGO_DEBUG")))

if DEBUG:
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS").split(",")

INTERNAL_IPS = [
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:{{cookiecutter.local_nginx_port}}',
    'http://127.0.0.1:{{cookiecutter.local_nginx_port}}',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.core',
    'apps.my_app',
    'rest_framework',
    'django_htmx',
    'tailwind',
    'theme',
    "django_cotton",
    'django_extensions',
    'widget_tweaks',
    'django_minify_html',
    'huey.contrib.djhuey',
    'django_json_widget',
    'django_prometheus',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        'livereload',
        'nplusone.ext.django',
    ]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django_minify_html.middleware.MinifyHtmlMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]


if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        'livereload.middleware.LiveReloadScript',
        'nplusone.ext.django.NPlusOneMiddleware',
    ]


if not DEBUG:
    try:
        auth_index = MIDDLEWARE.index(
            'django.contrib.auth.middleware.AuthenticationMiddleware')
        MIDDLEWARE.insert(
            auth_index + 1, 'django.contrib.auth.middleware.LoginRequiredMiddleware')
    except ValueError:
        MIDDLEWARE.append(
            'django.contrib.auth.middleware.LoginRequiredMiddleware')


ROOT_URLCONF = 'config.urls'
TAILWIND_APP_NAME = 'theme'


def get_npm_bin_path():
    npm_path = shutil.which("npm")

    if npm_path:
        return npm_path
    else:
        if platform.system() == "Windows":
            return r"C:\Program Files\nodejs\npm.cmd"
        else:
            return "~/.config/nvm/versions/node/v20.18.1/bin/npm"


NPM_BIN_PATH = get_npm_bin_path()


DEBUG_TOOLBAR_CONFIG = {
    "ROOT_TAG_EXTRA_ATTRS": "hx-preserve"
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django_prometheus.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}


REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Where collectstatic puts files
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / Path('media')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rich": {"datefmt": "[%X]"},
    },
    "handlers": {
        "console": {
            "class": "rich.logging.RichHandler",
            "formatter": "rich",
            "level": "DEBUG",
            "rich_tracebacks": True,
            "tracebacks_show_locals": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.security.BadRequest": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        'nplusone': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
