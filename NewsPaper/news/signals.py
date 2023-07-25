from django.db.models.signals import post_save, m2m_changed
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import *


def send_msg(previw, pk, title, subscribers_email):

    html_content = render_to_string(
        'flatpages/new_post.html',
        {
            'text': previw,
            'link': f'127.0.0.1:8000/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        print(instance)
        categories = instance.postCategory.all()
        subscribers_emails: list[str] = []
        for cat in categories:
            subscribers = Subscription.objects.filter(category=cat)
            subscribers_emails += [subs.user.email for subs in subscribers]
            print(subscribers_emails)

        send_msg(instance.previw(), instance.pk, instance.title, subscribers_emails)