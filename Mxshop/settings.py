"""
Django settings for Mxshop project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
# 如何将多个app放到一个文件夹apps（apps所在位置为项目根目录）下：
# 在settings.py文件中，insert apps路径即可
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
#告诉项目xadmin的导入路径
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'Mxshop'))
# print(sys.path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_n5b%%mm%+0vo!6f80(tk6wmit&g_rnl#^n88!zrr9k!i4^5uh'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 指定验证所需的用模型，UserProfile已经将之前
# 的user类继承了，所以不必担心完整性
# AUTH_USER_MODEL = "user.UserProfile"
ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'users.UserProfile'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'extra_apps.DjangoUeditor',
    'apps.users.apps.UsersConfig',
    'apps.goods.apps.GoodsConfig',
    'apps.trade.apps.TradeConfig',
    'apps.user_operation.apps.UserOperationConfig',

    'crispy_forms',
    'extra_apps.xadmin',
    'rest_framework',
    'django_filters',
    'corsheaders',

    'rest_framework.authtoken',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost:8080', # 请求的域名
)

ROOT_URLCONF = 'Mxshop.urls'

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

WSGI_APPLICATION = 'Mxshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mxshop_shop',
        'USER': 'root',
        'PASSWORD': 'yb1122yb',
        'HOST': "127.0.0.1",
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB'},
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'#修改为中文界面，1.8之前是zn-cn，

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
REST_FRAMEWORK = {
    #配置全局过滤器后端
    # 'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    #配置全局分页器
    'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE':5,
    "DEFAULT_AUTHENTICATION_CLASSES":(
      "rest_framework.authentication.BasicAuthentication",
      "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",#此处为全局配置token验证，
        #建议不要设置全局，可单独在需要token验证的view里添加：
        # from rest_framework.authentication import TokenAuthentication
        # authentication_classes = (TokenAuthentication,)
    ),

}
APIKEY = '9b11127a9701975c734b8aee81ee3526'
REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'

AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)
MEDIA_URL = '/media/'   #指定浏览url
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'Mxshop/media')#指定文件根目录

#设置缓存
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_OBJECT_CACHE_KEY_FUNC':
      'rest_framework_extensions.utils.default_object_cache_key_func',
    'DEFAULT_LIST_CACHE_KEY_FUNC':
      'rest_framework_extensions.utils.default_list_cache_key_func',
    #DRF的缓存时间设置
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15
}






















