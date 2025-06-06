import datetime

from celery import shared_task
from celery.utils.log import get_task_logger
from sentry_sdk import capture_exception

from apps.main.models import PlannedPosts
from apps.main.utils import send_posts, chennal_check_and_delay, update_chennal_last_send_msg
import time

logger = get_task_logger(__name__)


@shared_task(bind=True, queue='serial_queue')
def publish_post(self, planned_post_id: int):
    try:
        planned_post = PlannedPosts.objects.get(id=planned_post_id)
    except PlannedPosts.DoesNotExist:
        return "Planned post not published because not found"
    post_id = planned_post.post_id

    raise_error = False
    for p_post in planned_post.chennals.all():
        try:
            # chennal_check_and_delay(p_post.channel_username)
            # update_chennal_last_send_msg(p_post.channel_username)
            time.sleep(5)
            send_posts(chat=p_post.channel_username, post_id=post_id)
        except Exception as e:
            capture_exception(e)
            raise_error = True
    if raise_error:
        return "Not fully complated"
