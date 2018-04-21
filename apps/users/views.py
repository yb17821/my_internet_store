from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets
from .serializers import UserRegSerializer, SmsSerializer, UserDetailSerizlizer, UserChangePwdSerializer
from rest_framework.response import Response
from rest_framework import status
from utils.yunpian import YunPian
from Mxshop import settings
import random
from utils.permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import VerifyCode
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

# Create your views here.
User = get_user_model()
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class UserChangePwdViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = UserChangePwdSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    # def get_object(self):
    #     return self.request.user


class UserViewset(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  # mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    # serializer_class = UserRegSerializer
    # 动态设置serializer
    def get_serializer_class(self):

        if self.action == 'retrieve':
            return UserDetailSerizlizer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerizlizer

    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication,)

    # 动态设置permission
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        elif self.action == 'create':
            return [AllowAny()]
        elif self.action == 'updata' or 'destory':
            return [IsAuthenticated()]
        return [AllowAny()]

    # 重载create，实现注册完自动登录
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # 这个页面所有人可访问，但是又不能让所有人看到内容，所以，删除List功能

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送短信验证码
    '''
    serializer_class = SmsSerializer

    def generate_code(self):
        seeds = '1234567890'
        random_list = []
        for i in range(4):
            random_list.append(random.choice(seeds))
        return ''.join(random_list)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # raise_exception=True,如果出现异常，直接抛异常
        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(api_key=settings.APIKEY)
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code, mobile)
        if sms_status != 0:
            return Response({
                'mobile': sms_status['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response(
                {
                    'mobile': mobile
                }, status=status.HTTP_201_CREATED)


from django.contrib.auth import settings
from .models import UserProfile,WeiboAndUser
from django.contrib.auth.hashers import make_password
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.http.response import HttpResponse
import json
import requests
import random
def loginweibo(request):
    url = settings.WEIBO_GET_CODE_URL % (settings.WEIBO_KEY, settings.WEIBO_REDIRECT_URL)

    return redirect(url)

def completeweibo(request):
    code = request.GET.get('code')  # 获取code
    if not code:
        return redirect('/')
    data = {
        'code': code,
        'client_id': settings.WEIBO_KEY,
        'redirect_uri': settings.WEIBO_REDIRECT_URL,
        'client_secret': settings.WEIBO_SECRET,
    }

    response = json.loads(requests.post(settings.WEIBO_GET_TOKEN_URL, data=data).text)
    access_token = response.get('access_token') # 获取token
    weibo_id = response.get('uid') # 获取uid
    user_info_url = settings.WEIBO_GET_USER_INFO_URL % (access_token, weibo_id)
    weibo_user_info = json.loads(requests.get(user_info_url).text)
    weibo_name = weibo_user_info.get('screen_name')
    weiboanduser = WeiboAndUser.objects.filter(weibo_id = weibo_id)
    if  weiboanduser.exists():
        user = UserProfile.objects.get(id=weiboanduser[0].user_id)
        user.username = 'weibo'+weibo_name
        user.save()
    else:

        password = []
        for i in range(30):
            password.append(random.choice('abvdefghijklmnopqrstuvwxyz'))

        password = make_password(''.join(password))
        user = UserProfile.objects.create(username='weibo'+weibo_name, password=password, is_active=1, )
        print(weibo_id,user.id,'weibo'+weibo_name,password)
        WeiboAndUser.objects.create(weibo_id=weibo_id,user_id=user.id)


    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return  HttpResponse(token)



class CompleteweiboViewset(APIView):

    def get(self, request,format=None):
        code = self.request.query_params.get('code')  # 获取code
        if not code:
            return redirect('/')
        data = {
            'code': code,
            'client_id': settings.WEIBO_KEY,
            'redirect_uri': settings.WEIBO_REDIRECT_URL,
            'client_secret': settings.WEIBO_SECRET,
        }

        response = json.loads(requests.post(settings.WEIBO_GET_TOKEN_URL, data=data).text)
        access_token = response.get('access_token') # 获取token
        weibo_id = response.get('uid') # 获取uid
        user_info_url = settings.WEIBO_GET_USER_INFO_URL % (access_token, weibo_id)
        weibo_user_info = json.loads(requests.get(user_info_url).text)
        weibo_name = weibo_user_info.get('screen_name')
        weiboanduser = WeiboAndUser.objects.filter(weibo_id = weibo_id)
        if  weiboanduser.exists():
            user = UserProfile.objects.get(id=weiboanduser[0].user_id)
            user.username = 'weibo'+weibo_name
            user.save()
        else:

            password = []
            for i in range(30):
                password.append(random.choice('abvdefghijklmnopqrstuvwxyz'))

            password = make_password(''.join(password))
            user = UserProfile.objects.create(username='weibo'+weibo_name, password=password, is_active=1, )
            print(weibo_id,user.id,'weibo'+weibo_name,password)
            WeiboAndUser.objects.create(weibo_id=weibo_id,user_id=user.id)
        token, created = Token.objects.get_or_create(user=user)
        res = Response({'Token ': token.key})
        res.set_cookie('name',user.username,max_age=600)
        res.set_cookie('Authorization', 'Token '+token.key)
        return res


