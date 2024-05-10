from celery import shared_task
from celery.utils.log import get_task_logger

from apps.main.models import PlannedPosts
from apps.main.utils import send_posts

logger = get_task_logger(__name__)


@shared_task
def publish_post(planned_post_id: int):
    errors = []
    successes = []
    try:
        planned_post = PlannedPosts.objects.get(id=planned_post_id)

    except PlannedPosts.DoesNotExist:
        return "Planned post not published because not found"

    post = planned_post.post
    for p_post in planned_post.chennals.all():
        try:
            resp = send_posts(chat=p_post.channel_username, post=post)
            successes.append(resp)
        except Exception as e:
            errors.append(e)
    planned_post.was_posted = True
    planned_post.save()
    return {
        "successes": successes,
        "errors": errors,
    }
