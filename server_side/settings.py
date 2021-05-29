"""
Django settings for server_side project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import dj_database_url
import django_heroku
from pathlib import Path

import stripe
from decouple import config
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

ADMINS = [(config("MY_NAME"), config("MY_EMAIL"))]

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "server_side.apps.data_interaction.apps.DataInteractionConfig",
    "server_side.apps.main_interaction.apps.MainInteractionConfig",
    "server_side.apps.module_interaction.apps.ModuleInteractionConfig",
    "server_side.apps.shared_logic.apps.SharedLogicConfig",
    "admin_reorder",
    "smuggler",
    "django_rq"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
]

ROOT_URLCONF = "server_side.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "server_side.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(conn_max_age=600, default=config("DB_ID"))
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", _("English")),
    ("uk", _("Ukrainian")),
    ("de", _("German")),
    ("ru", _("Russian")),
    ("be", _("Belarusian")),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

ADMIN_REORDER = (
    "Data for administrator",
    {
        "app": "data_interaction",
        "label": _("groups_admin"),
        "models": ("data_interaction.AdminAction",),
    },
    {
        "app": "data_interaction",
        "label": _("profiles"),
        "models": (
            "auth.User",
            "data_interaction.Profile",
            "data_interaction.UserReview",
            "data_interaction.UserQuestion",
            "data_interaction.Company",
            "data_interaction.Workplace",
        ),
    },
    {
        "app": "data_interaction",
        "label": _("disasters"),
        "models": (
            "data_interaction.Disaster",
            "data_interaction.DisasterType",
            "data_interaction.DisasterTypeTranslation",
        ),
    },
    {
        "app": "data_interaction",
        "label": _("advices"),
        "models": (
            "data_interaction.Advice",
            "data_interaction.AdviceTranslation",
            "data_interaction.AdviceRating",
        ),
    },
    {
        "app": "data_interaction",
        "label": _("articles"),
        "models": ("data_interaction.Article", "data_interaction.ArticleRating"),
    },
    {
        "app": "data_interaction",
        "label": _("markets"),
        "models": ("data_interaction.Market", "data_interaction.MarketTranslation"),
    },
    {
        "app": "data_interaction",
        "label": _("target_audiences"),
        "models": (
            "data_interaction.TargetAudience",
            "data_interaction.TargetAudienceType",
            "data_interaction.TargetAudienceTypeTranslation",
        ),
    },
    {
        "app": "data_interaction",
        "label": _("forecasts"),
        "models": (
            "data_interaction.MarketForecast",
            "data_interaction.CompanyForecast",
            "data_interaction.CompanyStressTest",
            "data_interaction.TargetAudienceBehaviour",
        ),
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(name)-12s %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "file": {
            "level": ["DEBUG", "ERROR"],
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "logs/dismart_admin.log",
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
        },
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["console", "file"], "propagate": True},
        "django.request": {"level": ["DEBUG", "ERROR"], "handlers": ["file", "console"]},
        "django.db.backends": {"level": ["DEBUG", "ERROR"], "handlers": ["file"]},
        "django.template": {"level": ["DEBUG", "ERROR"], "handlers": ["file"]},
        "server_side.apps.shared_logic.loggers.view_status_logger": {
            "level": ["DEBUG", "ERROR"],
            "handlers": ["console", "file"],
        },
        "server_side.apps.shared_logic.loggers.class_status_logger": {
            "level": ["DEBUG", "ERROR"],
            "handlers": ["console", "file"],
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": None,
    "site_header": None,
    "site_logo": "images/logod.png",
    "site_logo_classes": "img-circle",
    "site_icon": "images/icond.jpg",
    "welcome_sign": _("Welcome"),
    "copyright": "Artem Khovrat",
    "search_model": "auth.User",
    "user_avatar": None,
    "topmenu_links": [
        {"name": _("Home"), "url": "admin:index", "permissions": ["auth.view_user"]},
        {
            "name": _("Open_client"),
            "url": "https://dismart.herokuapp.com",
            "new_window": True,
        },
        {"model": "auth.User"},
        {"app": "data_interaction"},
    ],
    "usermenu_links": [
        {
            "name": _("Download_Backup"),
            "url": "/admin/dump/",
            "permissions": ["auth.view_user"],
            "icon": "fas fa-cloud-download-alt",
        },
        {
            "name": _("Upload_Backup"),
            "url": "/admin/load/",
            "permissions": ["auth.view_user"],
            "icon": "fas fa-cloud-upload-alt",
        },
        {
            "name": _("Watch_Logs"),
            "url": "/admin/logs/watch/",
            "permissions": ["auth.view_user"],
            "icon": "fas fa-eye",
        },
        {
            "name": _("Download_Logs"),
            "url": "/admin/logs/download/",
            "permissions": ["auth.view_user"],
            "icon": "fas fa-download",
        },
        {
            "name": _("Open_Google"),
            "url": "http://google.com",
            "new_window": True,
            "icon": "fab fa-google",
        },
        {
            "name": _("Open_Github"),
            "url": "https://github.com/khovrat/dismart_admin",
            "new_window": True,
            "icon": "fab fa-github",
        },
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": ["main_interaction", "module_interaction", "shared_logic"],
    "hide_models": [],
    "order_with_respect_to": [
        "auth",
        "data_interaction.profile",
        "data_interaction.userreview",
        "data_interaction.userquestion",
        "data_interaction.workplace",
        "data_interaction.company",
        "data_interaction.disaster",
        "data_interaction.disastertype",
        "data_interaction.disastertypetranslation",
        "data_interaction.advice",
        "data_interaction.advicetranslation",
        "data_interaction.advicerating",
        "data_interaction.article",
        "data_interaction.articlerating",
        "data_interaction.market",
        "data_interaction.markettranslation",
        "data_interaction.targetaudience",
        "data_interaction.targetaudiencetype",
        "data_interaction.targetaudiencetypetranslation",
        "data_interaction.marketforecast",
        "data_interaction.companyforecast",
        "data_interaction.companystresstest",
        "data_interaction.targetaudiencebehaviour",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "data_interaction.profile": "fa fa-address-card",
        "data_interaction.disaster": "fa fa-bomb",
        "data_interaction.advice": "fa fa-bookmark",
        "data_interaction.article": "fa fa-book",
        "data_interaction.market": "fa fa-globe",
        "data_interaction.targetaudience": "fa fa-user-secret",
        "data_interaction.marketforecast": "fa fa-briefcase",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fa fa-genderless",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}

SECURE_SSL_REDIRECT = not DEBUG

SECURE_HSTS_SECONDS = 3600

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_USE_TLS = True

EMAIL_PORT = 587

EMAIL_HOST_USER = config("EMAIL_HOST_USER")

EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

stripe.api_key = config("STRIPE_API_KEY")

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': 'some-password',
        'DEFAULT_TIMEOUT': 360,
    },
    'with-sentinel': {
        'SENTINELS': [('localhost', 26736), ('localhost', 26737)],
        'MASTER_NAME': 'redismaster',
        'DB': 0,
        'PASSWORD': 'secret',
        'SOCKET_TIMEOUT': None,
        'CONNECTION_KWARGS': {
            'socket_connect_timeout': 0.3
        },
    },
    'high': {
        'URL': os.getenv('REDISTOGO_URL', 'redis://localhost:6379/0'), # If you're on Heroku
        'DEFAULT_TIMEOUT': 500,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    }
}

django_heroku.settings(locals())
