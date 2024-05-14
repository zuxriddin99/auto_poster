from celery import shared_task
from celery.utils.log import get_task_logger

from apps.main.models import PlannedPosts
from apps.main.utils import send_posts

logger = get_task_logger(__name__)


@shared_task
def publish_post(planned_post_id: int):
    errors = []
    successes = []
    print(14)
    try:
        planned_post = PlannedPosts.objects.get(id=planned_post_id)
        print(17)
    except PlannedPosts.DoesNotExist:
        return "Planned post not published because not found"
    post_id = planned_post.post_id
    # try:
    for p_post in planned_post.chennals.all():
        try:
            resp = send_posts(chat=p_post.channel_username, post_id=post_id)
            successes.append(resp)
        except Exception as e:
            errors.append(e)
    # except Exception as e:
    #     print(e)
    print(successes, errors)
    return {
        "successes": successes,
        "errors": errors,
    }
