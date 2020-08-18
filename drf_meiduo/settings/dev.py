"""
Django settings for drf_meiduo project.

Generated by 'django-admin startproject' using Django 1.11.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_path = os.path.join(BASE_DIR,'apps')
sys.path.insert(0,app_path)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jk1ydk&6vzt!r7i@p61c_75s%2-zt2%xvs(q1t#^y8q(v(b9v%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['api.meiduo.site:8080','127.0.0.1:8080']
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_extensions',
    'area.apps.AreaConfig',
    'users.apps.UsersConfig',
    'contents',
    'goods',
    'pictest',
    'ckeditor', #注册富文本编辑器
    'ckeditor_uploader'   #组测上传图片模块

]

MIDDLEWARE = [
    # 添加跨域请求中间键
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 添加请求白名单
CORS_ORIGIN_WHITELIST= (
    'http://127.0.0.1:8080',
    'http://www.meiduo.site:8080',
)
CORS_ALLOW_CREDENTIALS = True      # 允许携带cookie

ROOT_URLCONF = 'drf_meiduo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'drf_meiduo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drf_meiduo',
        'HOST': '192.168.133.1',
        'PORT': 3306,
        'USER': 'wangjun',
        'PASSWORD': 'wangjun'
    }
}


# drf 配置
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # 引入jwt认证
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

JWT_AUTH = {
    #设置JWT有效时间
    'JWT_EXPIRATION_DELTA':datetime.timedelta(days=1),
    'JWT_RESPONSE_PAYLOAD_HANDLER':'users.utils.jwt_response_paylod_handler'
}

# 指定自定义的后端认证
AUTHENTICATION_BACKENDS = {
    'users.utils.UsernameMobileAuthBackend'
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]


#声明使用自定义的User模型类
AUTH_USER_MODEL= 'users.User'

# Django框架的缓存设置，默认Django框架的缓存为服务器的内存，此处将Django框架的缓存改为了redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.59.129:63791/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # session 保存位置
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.59.129:63791/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    # 短信验证码保存位置
    "sms_code":{
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.59.129:63791/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
# 设置将session信息存储到缓存中，上面已经将缓存改为了redis，所有session会存放到redis中
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# 指定session存储到缓存空间的名称
# SESSION_CACHE_ALIAS = "session"


# 发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '18212707348@163.com'
EMAIL_HOST_PASSWORD = 'XXSJSWBSYBHMGEPG'
EMAIL_FROM = 'wangjun<18212707348@163.com>'


# 视图缓存配置
REST_FRAMEWORK_EXTENSIONS = {
    # 不缓存报错
    'DEFAULT_CACHE_ERRORS': False,
    # 指定key_func 函数
    # 'DEFAULT_CACHE_KEY_FUNC': 'rest_framework_extensions.utils.default_cache_key_func',
    # 指定缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 15,
    # 指定缓存配置
    'DEFAULT_USE_CACHE': 'session'
}

#指定fasffds 配置文件
FDFS_CLIENT_CONF = os.path.join(BASE_DIR,'utils/fastdfs/client.conf')
# 请求路径前缀
FDFS_URL= '192.168.59.129:8888/'
# 指定django 使用的文件存储类
DEFAULT_FILE_STORAGE = 'drf_meiduo.utils.fastdfs.storage.FDFSStorage'

# 富文本编辑器ckeditor配置
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',  # 工具条功能
        'height': 300,  # 编辑器高度
        # 'width': 300,  # 编辑器宽
    },
}

CKEDITOR_UPLOAD_PATH = '' #上传图片路径，使用了fdfs 所以为''

# 生成的静态html文件保存目录
GENERATED_STATIC_HTML_FILES_DIR = os.path.join(os.path.dirname(BASE_DIR), 'front_end_pc')