import asyncio
from asgiref.sync import async_to_sync
from django_celery_beat.models import PeriodicTask, PeriodicTasks

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from apps.main.adapters import bot
from apps.main.logics import generate_name
from config.settings import BOT_ID


class Post(models.Model):
    class PostStatusEnum(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending'
        PUBLISHED = 'published', 'Published'

    class PostTypeEnum(models.TextChoices):
        TEXT = 'text', 'Text'
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        ALBUM = 'album', 'Album'

    post_type = models.CharField(choices=PostTypeEnum.choices, max_length=20, default=PostTypeEnum.TEXT.value)
    content = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PostStatusEnum.choices, default=PostStatusEnum.DRAFT)

    class Meta:
        db_table = 'posts'


class PostMedia(models.Model):
    class MediaTypeEnum(models.TextChoices):
        VIDEO = 'video', 'Video'
        IMAGE = 'image', 'Image'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='medias')
    media_type = models.CharField(max_length=20, choices=MediaTypeEnum.choices, default=MediaTypeEnum.IMAGE.value)
    file = models.FileField(upload_to='medias')

    class Meta:
        db_table = 'postmedias'


class TelegramChennels(models.Model):
    channel_name = models.CharField(max_length=100, null=True)
    channel_username = models.CharField(max_length=100, null=True)
    chenel_id = models.CharField(max_length=100, blank=True, null=True)
    has_access = models.BooleanField(default=False)

    class Meta:
        db_table = 'telegram_chennels'

    def __str__(self):
        return f'{self.channel_name}({self.channel_username})'

    def save(self, *args, **kwargs):
        # a = bot.get_chat_member(chat_id=self.channel_username, user_id=BOT_ID)
        # if a.status == 'administrator':
        super(TelegramChennels, self).save(*args, **kwargs)
        # else:


class PlannedPosts(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='planned_posts')
    chennals = models.ManyToManyField(TelegramChennels, related_name='planned_posts')
    datetime_posting = models.DateTimeField()
    was_posted = models.BooleanField(default=False)

    class Meta:
        db_table = 'planned_posts'

    def save(self, *args, **kwargs):
        super(PlannedPosts, self).save(*args, **kwargs)
        PeriodicTask.objects.create(
            name=f"Publish post_id:{self.post_id}. ({generate_name()})",
            task="apps.main.tasks.publish_post",
            one_off=True,
            start_time=self.datetime_posting,
            crontab_id=2,
            kwargs=f'{{"planned_post_id": {self.id}}}'
        )
