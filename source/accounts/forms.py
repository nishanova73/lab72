from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model

from .models import AuthToken, Profile, TOKEN_TYPE_PASSWORD_RESET


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2',
                  'first_name', 'last_name', 'email']

    def save(self, commit=True):
        if settings.ACTIVATE_USERS_EMAIL:
            user: AbstractUser = super().save(commit=False)
            user.is_active = False
            if commit:
                user.save()
                token = self.create_token(user)
                self.send_email(user, token)
        else:
            user = super().save(commit=commit)
            Profile.objects.create(user=user)
        return user

    def create_token(self, user):
        return AuthToken.objects.create(user=user)

    def send_email(self, user, token):
        if user.email:
            subject = 'You created an account on page "Quotes"'
            link = settings.BASE_HOST + reverse('accounts:activate', kwargs={'token': token.token})
            message = f'''hello, {user.username}!
You created an account on page "Quotes"
Activate it on this page {link}'''
            html_message = f'''hello, {user.username}!
You created an account on page "Quotes"
Activate it on this page <a href="{link}">{link}</a>'''
            try:
                user.email_user(subject, message, html_message=html_message)
            except Exception as e:
                print(e)

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'Name', 'last_name': 'Last name', 'email': 'Email'}


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class SetPasswordForm(forms.ModelForm):
    password = forms.CharField(label="New password", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Enter password again", widget=forms.PasswordInput, strip=False)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords are not similar!')
        return password_confirm

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm']


class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(label="Old password", strip=False, widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Old password is incorrect!')
        return old_password

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']


class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField(required=True, label='Email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        if User.objects.filter(email=email).count() == 0:
            raise ValidationError("User doesn't have such email")
        return email

        def send_email(self):
            User = get_user_model()
            email = self.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            token = AuthToken.objects.create(user=user, life_days=3, type=TOKEN_TYPE_PASSWORD_RESET)

            subject = 'You asked resetting your password on "quote" page ""'
            link = settings.BASE_HOST + reverse('accounts:password_reset', kwargs={'token': token.token})
            message = f'''Link for resetting password: {link}'''
            html_message = f'''Link for resetting password: <a href="{link}">{link}</a>'''
            try:
                user.email_user(subject, message, html_message=html_message)
            except Exception as e:
                print(e)


class PasswordResetForm(SetPasswordForm):
    pass