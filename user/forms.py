from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'登录用户名或邮箱！'}))
    userpass = forms.CharField(label='密　码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'登录密码'}))

    def clean(self):
        username = self.cleaned_data['username_or_email']
        userpass = self.cleaned_data['userpass']
        user = auth.authenticate(username=username, password=userpass)
        if user is None:
            if User.objects.filter(email=username).exists():
                username = User.objects.get(email=username).username
                user = auth.authenticate(username=username, password=userpass)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或密码错误！')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegForm(forms.Form):
    username = forms.CharField(label='用 户 名', max_length=30, min_length=4, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'输入登录用户名'}))
    email = forms.EmailField(label='邮箱地址', widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'输入邮箱地址'}))
    verify_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}))
    userpass = forms.CharField(label='密　　码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'输入登录密码'}))
    passagain = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'输入确认密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegForm, self).__init__(*args, **kwargs)

    def clean(self):
        code = self.request.session.get('register_code', '')
        verify_code = self.cleaned_data.get('verify_code', '')
        if not (code != '' and code == verify_code):
            raise forms.ValidationError('验证码不正确！')

        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱地址已存在！')
        return email

    def clean_passagain(self):
        userpass = self.cleaned_data['userpass']
        passagain = self.cleaned_data['passagain']
        if userpass != passagain:
            raise forms.ValidationError('两次输入的密码不一致！')
        return passagain

    def clean_verify_code(self):
        verify_code = self.cleaned_data.get('verify_code', '').strip()
        if verify_code == '':
            raise forms.ValidationError('请输入验证码！')
        return verify_code

class EditForm(forms.Form):
    nickname = forms.CharField(label='昵称', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'修改昵称'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(EditForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname', '').strip()
        if nickname == '':
            raise forms.ValidationError('请输入昵称')
        return nickname

class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}))
    verify_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        code = self.request.session.get('bind_email_code', '')
        verify_code = self.cleaned_data.get('verify_code', '')
        if not (code != '' and code == verify_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email

    def clean_verify_code(self):
        verify_code = self.cleaned_data.get('verify_code', '').strip()
        if verify_code == '':
            raise forms.ValidationError('请输入验证码！')
        return verify_code

class EditPassForm(forms.Form):
    old_pass = forms.CharField(label='旧 密 码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入旧密码！'}))
    new_pass = forms.CharField(label='新 密 码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入新密码！'}))
    aga_pass = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入确认密码！'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(EditPassForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_pass = self.cleaned_data.get('new_pass', '')
        aga_pass = self.cleaned_data.get('aga_pass', '')
        if new_pass != aga_pass or new_pass == '':
            raise forms.ValidationError('两次输入的密码不一致！')
        return self.cleaned_data

    def clean_old_pass(self):
        old_pass = self.cleaned_data.get('old_pass', '')
        if not self.user.check_password(old_pass):
            raise forms.ValidationError('旧密码输入错误！')
        return old_pass

class FindPassForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入绑定邮箱'}))
    verify_code = forms.CharField(label='验证码', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'点击“发送验证码”发送到邮箱'}))
    new_pass = forms.CharField(label='新密码', min_length=6, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'输入新密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(FindPassForm, self).__init__(*args, **kwargs)

    def clan_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在！')
        return email

    def clean_verify_code(self):
        verify_code = self.cleaned_data.get('verify_code', '').strip()
        if verify_code == '':
            raise forms.ValidationError('请输入验证码！')
        code = self.request.session.get('find_pass_code', '')
        print(code)
        verify_code = self.cleaned_data.get('verify_code', '')
        if not (code != '' and code == verify_code):
            raise forms.ValidationError('验证码不正确！')
        return verify_code