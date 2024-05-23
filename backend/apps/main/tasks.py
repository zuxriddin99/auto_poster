from celery import shared_task
from celery.utils.log import get_task_logger

from apps.main.models import PlannedPosts
from apps.main.utils import send_posts
import time
logger = get_task_logger(__name__)


@shared_task
def publish_post(planned_post_id: int):
    try:
        planned_post = PlannedPosts.objects.get(id=planned_post_id)
    except PlannedPosts.DoesNotExist:
        return "Planned post not published because not found"
    post_id = planned_post.post_id
    for p_post in planned_post.chennals.all():
        time.sleep(0.5)
        # try:
        send_posts(chat=p_post.channel_username, post_id=post_id)
        # except Exception as e:
        #     pass