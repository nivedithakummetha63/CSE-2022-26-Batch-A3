"""
Django settings for roomieradar project.
Institute-level Roomie Radar System
"""

from pathlib import Path
import os

# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------
# SECURITY SETTINGS
# --------------------------------------------------

SECRET_KEY = 'django-insecure-roomieradar-local-dev-key'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# --------------------------------------------------
# APPLICATION DEFINITION
# --------------------------------------------------

INSTALLED_APPS = [
    'jazzmin',
    
    # Django default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project apps
    'accounts',
    'base',
    'chat',
    'roomieradar_app',
    'home',
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'roomieradar.middleware.AdminRedirectMiddleware',  # Custom admin redirect
]


# --------------------------------------------------
# URL CONFIGURATION
# --------------------------------------------------

ROOT_URLCONF = 'roomieradar.urls'


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global templates
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


# --------------------------------------------------
# WSGI APPLICATION
# --------------------------------------------------

WSGI_APPLICATION = 'roomieradar.wsgi.application'


# --------------------------------------------------
# DATABASE (SQLite – Institute Level)
# --------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True
USE_TZ = True


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


# --------------------------------------------------
# MEDIA FILES
# --------------------------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --------------------------------------------------
# AUTHENTICATION SETTINGS
# --------------------------------------------------

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/app/'
LOGOUT_REDIRECT_URL = '/'


# --------------------------------------------------
# EMAIL CONFIGURATION
# --------------------------------------------------

# SMTP backend for real email sending
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'nivedithakummetha@gmail.com'
EMAIL_HOST_PASSWORD = 'uyrsbufaazomitic'


# Custom sender name and email
DEFAULT_FROM_EMAIL = 'Roomie Radar <noreply@roomieradar.com>'
SERVER_EMAIL = 'Roomie Radar <noreply@roomieradar.com>'

# Additional email settings
EMAIL_SUBJECT_PREFIX = '[Roomie Radar] '
ADMINS = [('Roomie Radar Admin', 'admin@roomieradar.com')]


# --------------------------------------------------
# SITE URL (Used in Email Links)
# --------------------------------------------------

SITE_URL = 'http://127.0.0.1:8000'


# --------------------------------------------------
# SECURITY (REVIEW FRIENDLY)
# --------------------------------------------------

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True


# --------------------------------------------------
# DEFAULT PRIMARY KEY FIELD
# --------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --------------------------------------------------
# JAZZMIN ADMIN UI CONFIGURATION
# --------------------------------------------------

JAZZMIN_SETTINGS = {
    # Site branding
    "site_title": "Roomie Radar Admin",
    "site_header": "Roomie Radar",
    "site_brand": "Roomie Radar Admin Panel",
    "site_logo": "images/logo.png",
    "site_logo_classes": "",
    "site_icon": None,
    
    # Welcome text
    "welcome_sign": "Welcome to Roomie Radar Admin Dashboard",
    
    # Copyright
    "copyright": "Roomie Radar © 2024",
    
    # Search model
    "search_model": "auth.User",
    
    # User avatar
    "user_avatar": None,
    
    # Top menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],
    
    # User menu
    "usermenu_links": [
        {"model": "auth.user"}
    ],
    
    # Side menu ordering
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Custom links
    "custom_links": {
        "accounts": [{
            "name": "User Management",
            "url": "admin:auth_user_changelist",
            "icon": "fas fa-users",
            "permissions": ["auth.view_user"]
        }]
    },
    
    # Icons for models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "base.Profile": "fas fa-id-card",
        "base.Preferences": "fas fa-sliders-h",
        "chat.ChatRoom": "fas fa-comments",
        "chat.Message": "fas fa-comment",
        "chat.BlockedUser": "fas fa-ban",
        "chat.UserReport": "fas fa-flag",
        "roomieradar_app.Room": "fas fa-door-open",
        "roomieradar_app.Booking": "fas fa-calendar-check",
    },
    
    # Default icon for models
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related modal
    "related_modal_active": False,
    
    # Custom CSS/JS
    "custom_css": "admin/css/custom_admin.css",
    "custom_js": None,
    
    # Show language chooser
    "show_ui_builder": False,
    
    # Change form templates
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs"
    },
    
    # Language chooser
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-purple",
    "accent": "accent-primary",
    "navbar": "navbar-purple navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}


