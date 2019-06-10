import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.core.mail import send_mail
from blog.models import Blog
from .forms import LoginForm, RegForm, EditForm, BindEmailForm, EditPassForm, FindPassForm
from .models import Profile

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def detail_login(request):
    data = {}
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = True
    else:
        data['status'] = False
    return JsonResponse(data)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))

def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            userpass = reg_form.cleaned_data['userpass']
            user = User.objects.create_user(username, email, userpass)
            user.save()
            del request.session['register_code']
            user = auth.authenticate(username=username, password=userpass)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)

def edit_nickname(request):
    redirect_url = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        print(request.user)
        form = EditForm(request.POST, user=request.user)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname
            profile.save()
            return redirect(redirect_url)
    else:
        form = EditForm()
    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    return render(request, 'form.html', context)

def bind_email(request):
    redirect_url = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        print(request.user)
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            del request.session['bind_email_code']
            return redirect(redirect_url)
    else:
        form = BindEmailForm()
    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    return render(request, 'user/bind_email.html', context)

def send_verify_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email_code'] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '[流星承诺的博客]Email 地址验证',
                '验证码：%s' % code,
                '8699286@qq.com',
                [email],
                fail_silently=False,
            )
            data['static'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def edit_pass(request):
    redirect_url = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        form = EditPassForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            new_pass = form.cleaned_data['new_pass']
            user.set_password(new_pass)
            user.save()
            auth.logout(request)
            return redirect(redirect_url)
    else:
        form = EditPassForm()
    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    return render(request, 'form.html', context)

def find_pass(request):
    redirect_url = reverse('login')
    if request.method == 'POST':
        print(request.user)
        form = FindPassForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_pass = form.cleaned_data['new_pass']
            user = User.objects.get(email=email)
            user.set_password(new_pass)
            user.save()
            del request.session['find_pass_code']
            return redirect(redirect_url)
    else:
        form = FindPassForm()
    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    return render(request, 'user/find_pass.html', context)