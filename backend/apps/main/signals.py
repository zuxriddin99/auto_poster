from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.main.models import Post


@receiver(post_delete, sender=Post)
def post_delete_signal(sender, instance, **kwargs):
    post_id = instance.id
    PeriodicTask.objects.filter(kwargs=f'{{"planned_post_id": {post_id}}}', enabled=True).update(enabled=False)
