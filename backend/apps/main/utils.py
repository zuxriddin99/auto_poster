import datetime
import time

from django.core.cache import cache
from telebot import types

from apps.main.adapters import bot
from apps.main.models import Post
from config.settings import TIME_ZONE


def refactor_text(text: str):
    text = text.replace('<p>', '').replace('</p>', '\n')
    text = text.replace("<br>", "\n")
    text = text.replace("&nbsp;", " ")
    return text


def send_posts(chat: str, post_id):
    post = Post.objects.get(id=post_id)
    if post.post_code:
        copy_post(chat, post)
    else:
        functions = {
            Post.PostTypeEnum.TEXT: send_text_message,
            Post.PostTypeEnum.IMAGE: send_image_message,
            Post.PostTypeEnum.VIDEO: send_video_message,
            Post.PostTypeEnum.ALBUM: send_album_message
        }
        functions[post.post_type](chat, post_id)


def copy_post(chat: str, post: Post):
    from_chat_id, msg_id = post.post_code.split(",")
    try:
        bot.copy_message(chat_id=chat, from_chat_id=from_chat_id, message_id=msg_id)
    except Exception as e:
        if "retry after " in str(e):
            q = int(str(e).split('retry after ')[-1])
            time.sleep(q)
def send_text_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    text = refactor_text(text=post.content)
    try:
        bot.send_message(chat_id=chat, text=text, parse_mode="HTML")
    except Exception as e:
        if "retry after " in str(e):
            q = int(str(e).split('retry after ')[-1])
            time.sleep(q)

def send_image_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    text = refactor_text(text=post.content)
    image = post.medias.first()
    try:
        bot.send_photo(chat_id=chat, photo=image.file, caption=text, parse_mode="HTML")
    except Exception as e:
        if "retry after " in str(e):
            q = int(str(e).split('retry after ')[-1])
            time.sleep(q)

def send_video_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    text = refactor_text(text=post.content)
    video = post.medias.first()
    try:
        bot.send_video(chat_id=chat, video=video.file, caption=text, parse_mode="HTML")
    except Exception as e:
        if "retry after " in str(e):
            q = int(str(e).split('retry after ')[-1])
            time.sleep(q)

def send_album_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    medias = []
    for index, media in enumerate(post.medias.all()):
        caption = refactor_text(text=post.content) if index == 0 else None
        if media.media_type == "image":
            medias.append(types.InputMediaPhoto(media=media.file, caption=caption, parse_mode="HTML"))
        elif media.media_type == "video":
            medias.append(types.InputMediaVideo(media=media.file, caption=caption, parse_mode="HTML"))
    try:
        bot.send_media_group(chat_id=chat, media=medias)
    except Exception as e:
        if "retry after " in str(e):
            q = int(str(e).split('retry after ')[-1])
            time.sleep(q)

def cache_chennal_name_gen(username: str):
    return f"{username}_last_send_time"


def update_chennal_last_send_msg(username: str):
    cache.set(key=cache_chennal_name_gen(username), value=datetime.datetime.now())


def get_chennal_last_send_time(username: str):
    return cache.get(key=cache_chennal_name_gen(username), default=None)


def has_send_msg_to_chennal(username: str):
    last_msg_datetime = get_chennal_last_send_time(username)
    if last_msg_datetime:
        now = datetime.datetime.now()
        if (now - last_msg_datetime).total_seconds() >= 4:
            return True
    return False


def chennal_check_and_delay(username: str):
    time.sleep(2 if has_send_msg_to_chennal(username) else 3)
