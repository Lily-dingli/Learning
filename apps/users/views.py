from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

from apps.operations.models import UserProfile
from apps.users.forms import LoginForm,RegisterPostForm
from apps.users.forms import DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
from OnlineObjects.settings import yp_apikey, REDIS_HOST, REDIS_PORT
import redis


# CBV
# Create your views here.
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {'register_get_form': register_get_form})

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        dynamic_login = True
        if register_post_form.is_valid():
            # 没有注册帐号依然可以登录
            mobile =register_post_form.cleaned_data['mobile']
            password=register_post_form.cleaned_data['password']
            # code=login_form.cleaned_data['code']
            #         新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            register_get_form = RegisterGetForm()
            # register_post_form=RegisterPostForm()
            return render(request, 'register.html',{'register_get_form': register_get_form,
                                                    'register_post_form':register_post_form})
        # return render(request, 'register.html')


class DynamicLoginView(View):
    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            # 没有注册帐号依然可以登录
            mobile = login_form.cleaned_data['mobile']
            # code=login_form.cleaned_data['code']
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]

            else:
                #         新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            d_form = DynamicLoginForm()
            return render(request, 'login.html', {'login_form': login_form,
                                                  'd_form': d_form,
                                                  'dynamic_login': dynamic_login})


class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data['mobile']
            # 随机生成数字验证码
            code = generate_random(4, 0)
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json['code'] == 0:
                re_dict['status'] ='success'

                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset='utf8', decode_responses=True)
                r.set(mobile, code)
                r.expire(str(mobile), 60 * 5)  # 设置验证码5分钟过期
            else:
                re_dict['msg'] = re_json['msg']

        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        login_form = DynamicLoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request, *args, **kwargs):
        # form表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # 用于通过用户名查询用户是否存在
            user = authenticate(username=user_name, password=password)
            # from apps.users.models import UserProfile
            # 通过用户名查询用户
            # 需要先加密再通过加密之后密码查询
            # 对整个django后端后续代码不好
            # user=UserProfile.objects.get(username=user_name,password=password)
            if user is not None:
                #                        查询到用户
                login(request, user)
                #         登录成功之后应该怎么返回页面
                return HttpResponseRedirect(reverse('index'))
            else:
                #             未查询到用户
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})
