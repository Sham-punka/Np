from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMultiAlternatives, mail_managers
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        author = Group.objects.get(name="common_users")
        user.groups.add(author)

        mail_managers(subject='New user', message=f'New user {user.username} signup on site!')

        subject = 'Добро пожаловать на наш News Portal! '
        text = f'{user.username}, вы успешно зарегистрировались!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарениситрировались на '
            f'<a href="http://127.o.o.1:8000/news/search">сайте</a>!'
        )
        msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[user.email])
        msg.attach_alternative(html, "text/html")
        msg.send()

        return user