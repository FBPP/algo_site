import datetime
import pytz

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from . models import User
from . import models

def make_confirm_string(user):
    from uuid import uuid4
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%s")
    code = str(uuid4())
    models.ConfirmString.objects.create(code = code, user = user)
    return code

def regist(request):
    if request.method == "GET":
        context = {}
        context['prev_page'] = request.GET.get("from_page")
        return render(request, "register/register.html", context)
    else:
        name = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        context = {}
        flag = False
        if User.objects.filter(user_name = name).exists():
            context["error_name"] = "用户名已存在"
            flag = True
        if User.objects.filter(email = email).exists():
            context["error_email"] = "邮箱已存在"
            flag = True
        if flag:
            context['prev_page'] = request.POST.get("from_page")
            return render(request, "register/register.html", context)
        else:
            user = User.objects.create(user_name = name, password = password, email = email)
            user.save()
            code = make_confirm_string(user)
            send_email(email, code)
            message = "请前往注册邮箱, 进行邮件确认"
            return render(request, 'register/confirm.html', locals())
def send_email(email, code):
    from django.core.mail import EmailMultiAlternatives
    subject = "来自algo的注册邮件"
    text_content = "你的邮箱服务不支持html格式, 无法完成验证"
    html_content = ''' <h3>感谢注册</h3>
                    <p>点击<a href = "http://{}/register/confirm/{}" target = blank >www.register.link</a>完成注册确认</p>
                    <p> 此链接有效期为{} </p>
                    '''.format("172.20.10.11:8000", code, settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def confirm(request, code):
    message = ""
    try:
        confirm = models.ConfirmString.objects.get(code = code) 
    except:
        message = "无效的确认请求"
        return render(request, "register/confirm.html", locals())
    c_time = confirm.c_time
    now = datetime.datetime.now()
    now = now.replace(tzinfo = pytz.timezone("UTC"))
    if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message = "你的邮件已经过期, 请重新注册"
        return render(request, "register/confirm.html", locals())
    else:
        confirm.user.has_confirmed = True
        confirm.user.save()
        confirm.delete()
        message = "注册成功, 开始刷题之旅吧"
        return render(request, "register/confirm.html", locals())
def lg(request):
    if request.method == "GET":
        return render(request, "register/lg.html");
    else:
        email = request.POST["email"]
        password = request.POST["password"]
        context = {}
        flag = False
        if not User.objects.filter(email = email).exists():
            context["error_email"] = "邮箱不存在"
            flag = True
        else :
            u = models.User.objects.get(email = email)
            if not u.has_confirmed:
                flag = True
                context["error_email"] = "邮箱没有注册"
            if u.password != password:
                flag = True
                context["error_password"] = "密码错误"
        if flag:
            return render(request, "register/lg.html", context)
        else:
            request.session["email"] = email
            request.session["password"] = password

            return HttpResponseRedirect(reverse("algo:lg_index", args = (u.pk, )))