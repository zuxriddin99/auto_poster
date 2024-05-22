from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask

from apps.main.models import Post


@receiver(pre_delete, sender=Post)
def post_delete_signal(sender, instance, **kwargs):
    planned_posts_data = []
    for i in instance.planned_posts.all().values_list('id', flat=True):
        planned_posts_data.append(f'{{"planned_post_id": {i}}}')
    PeriodicTask.objects.filter(kwargs__in=planned_posts_data, enabled=True).update(enabled=False)
