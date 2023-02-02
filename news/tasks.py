from django.core.mail import EmailMultiAlternatives
from celery import shared_task


@shared_task
def send_mail_for_sub_once(sub_username, sub_useremail, html_content):
    print('старт')
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}. Новая статья в вашем разделе!',
        from_email='grigoryev0089@gmail.com',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')

    print()
    print(html_content)
    print()

    msg.send()
    print('конец')


@shared_task
def send_mail_every_week(sub_username, sub_useremail, html_content):
    print('Задача_много_писем - старт')
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}, новые статьи за прошлую неделю в вашем разделе!',
        from_email='grigoryev0089@gmail.com',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')
    print()

    print(html_content)

    msg.send()
    print('стоп')
