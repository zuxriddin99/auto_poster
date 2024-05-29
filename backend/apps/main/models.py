import asyncio
from asgiref.sync import async_to_sync
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule, CrontabSchedule

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from apps.main.adapters import bot
from apps.main.logics import generate_name
from config.settings import BOT_ID, timezone


class Post(models.Model):
    class PostTypeEnum(models.TextChoices):
        TEXT = 'text', 'Текст'
        IMAGE = 'image', 'Изображение'
        VIDEO = 'video', 'Видео'
        ALBUM = 'album', 'Альбом'

    post_type = models.CharField(
        verbose_name="Тип публикации", choices=PostTypeEnum.choices, max_length=20, default=PostTypeEnum.TEXT.value)
    content = CKEditor5Field(verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"


class PostMedia(models.Model):
    class MediaTypeEnum(models.TextChoices):
        VIDEO = 'video', 'Видео'
        IMAGE = 'image', 'Изображение'

    post = models.ForeignKey(
        Post, verbose_name="Публикация", on_delete=models.CASCADE, related_name='medias')
    media_type = models.CharField(
        verbose_name="Тип медиафайла", max_length=20, choices=MediaTypeEnum.choices, default=MediaTypeEnum.IMAGE.value)
    file = models.FileField(verbose_name="Файл", upload_to='medias')

    class Meta:
        db_table = 'postmedias'
        verbose_name = "Медиафайл публикации"
        verbose_name_plural = "Медиафайл публикаций"


class TelegramChennels(models.Model):
    channel_name = models.CharField(verbose_name="Название канала", max_length=100, unique=True, null=True)
    channel_username = models.CharField(verbose_name="Название канала(username)", max_length=100, unique=True, null=True)

    class Meta:
        db_table = 'telegram_chennels'
        verbose_name = "Телеграм-канал"
        verbose_name_plural = "Telegram-каналы"

    def __str__(self):
        return f'{self.channel_name}({self.channel_username})'


class PlannedPosts(models.Model):
    class IntervalEnum(models.TextChoices):
        NONE = '1', '----------'
        EVERY_1_MIN = 'every_1_minutes', 'Каждые 1 минут'
        EVERY_5_MIN = 'every_5_minutes', 'Каждые 5 минут'
        EVERY_10_MIN = 'every_10_minutes', 'Каждые 10 минут'
        EVERY_15_MIN = 'every_15_minutes', 'Каждые 15 минут'
        EVERY_20_MIN = 'every_20_minutes', 'Каждые 20 минут'
        EVERY_30_MIN = 'every_30_minutes', 'Каждые 30 минут'
        EVERY_1_HOUR = 'every_1_hours', 'Каждый 1 час'
        EVERY_2_HOUR = 'every_2_hours', 'Каждые 2 часа'
        EVERY_3_HOUR = 'every_3_hours', 'Каждые 3 часа'

    post = models.ForeignKey(Post, verbose_name="Публикация", on_delete=models.CASCADE, related_name='planned_posts')
    chennals = models.ManyToManyField(TelegramChennels, verbose_name="каналы", related_name='planned_posts')
    datetime_posting = models.DateTimeField(verbose_name="Дата и время отправки публикации")
    end_datetime_posting = models.DateTimeField(verbose_name="Истекает", blank=True, null=True)
    one_time_task = models.BooleanField("Одноразовая задача", default=True)
    interval = models.CharField(
        verbose_name="Интервал", max_length=20, choices=IntervalEnum.choices, default=IntervalEnum.NONE.value)

    class Meta:
        db_table = 'planned_posts'
        verbose_name = "Планируемая публикация"
        verbose_name_plural = "Планируемые публикации"

    def save(self, *args, **kwargs):
        is_created = not self.pk
        super(PlannedPosts, self).save(*args, **kwargs)
        if is_created:
            data = {
                "name": f"Publish post_id:{self.post_id}. (planned_post_id{self.id})",
                "task": "apps.main.tasks.publish_post",
                "start_time": self.datetime_posting,
                "interval": self.get_interval(),
                "crontab": self.get_crone_tab(),
                "kwargs": f'{{"planned_post_id": {self.id}}}'
            }
            if self.end_datetime_posting:
                data['expires'] = self.end_datetime_posting
            else:
                data["one_off"] = True
            PeriodicTask.objects.create(
                **data
            )

    def get_interval(self):
        if self.interval == self.IntervalEnum.NONE:
            return None
        every, period = self.interval_enum_to_data(self.interval)
        obj, _ = IntervalSchedule.objects.get_or_create(
            every=int(every),
            period=period
        )
        return obj

    @staticmethod
    def interval_enum_to_data(interval_enum: str):
        every, period = interval_enum.split("_")[-2:]
        return every, period

    def get_crone_tab(self):
        if self.interval == self.IntervalEnum.NONE:
            obj, _ = CrontabSchedule.objects.get_or_create(timezone=timezone, minute='*', hour='*',
                                                           day_of_month='*', month_of_year='*', day_of_week='*')
            return obj
        return None
