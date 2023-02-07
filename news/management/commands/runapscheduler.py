import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from datetime import datetime

from NewsPaper.news.models import Category, Post

logger = logging.getLogger(__name__)


# рассылка подписчикам новых новостей за прошлую неделю по определенным категориям новостей
def news_sender():
    # Первый цикл - получение из модели категории по очереди всех объектов, всех наименований категорий
    for category in Category.objects.all():

        # пустой список для будущего формирования списка статей, разбитых по категориям + ссылка перехода на каждую
        # статью, своя уникальная рядом с названием статьи
        news_from_each_category = []

        # определение номера прошлой недели
        week_number_last = datetime.now().isocalendar()[1] - 1

        # Второй цикл - из первого цикла получим рк категории, и подставляем его в запрос, в первый фильтр, во второй
        # фильтр подставляем значение предыдущей недели, то есть показать статьи с датой создания предыдущей недели
        for post in Post.objects.filter(post_category_id=category.id,
                                        time_of_creation__week=week_number_last).values('pk',
                                                                                        'title',
                                                                                        'time_of_creation',
                                                                                        'post_category_id__name'):
            # преобразуем дату в человеческий вид - убираем секунды и прочее
            date_format = post.get("time_of_creation").strftime("%d/%m/%Y")

            # из данных запроса выдираем нужные нам поля (time_of_creation - для проверки выводится),
            # и из значений данных полей формируем заголовок и реальную ссылку на переход на статью на наш сайт
            post = (f' http://127.0.0.1:8000/posts/{post.get("pk")}, Заголовок: {post.get("title")}, '
                    f' Категория: {post.get("postCategory_id__name")}, Дата создания: {date_format}')

            # каждую строчку помещаем в список новостей
            news_from_each_category.append(post)

        # переменная subscribers содержит информацию о подписчиках, в дальнейшем понадобится их мыло
        subscribers = category.subscribers.all()

        # Третий цикл - доформирование письма (имя кому отправляем получаем тут) и рассылка готового
        # письма подписчикам, которые подписаны под данной категорией
        # создаем приветственное письмо с нашим списком новых за неделю статей конкретной категории,
        # помещаем в письмо шаблон (html страничку), а также передаем в шаблон нужные нам переменные
        for subscriber in subscribers:
            subscriber_username = subscriber.username
            subscriber_email = subscriber.email
            html_content = render_to_string(
                'news/mail_sender.html', {'user': subscriber,
                                          'text': news_from_each_category,
                                          'category_name': category.name,
                                          'week_number_last': week_number_last})


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        scheduler.add_job(
            news_sender,
            trigger=CronTrigger(second="*/10"),
            id="news_sender",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работа 'news_sender'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Задачник запущен")
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Задачник остановлен")
            scheduler.shutdown()
            print('Задачник остановлен')
            logger.info("Задачник остановлен успешно!")
