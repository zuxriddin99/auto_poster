from telebot import types

from apps.main.adapters import bot
from apps.main.models import Post


def refactor_text(text: str):
    text = text.replace('<p>', '').replace('</p>', '\n')
    text = text.replace("<br>", "\n")
    text = text.replace("&nbsp;", " ")
    return text

def send_posts(chat: str, post_id):
    post = Post.objects.get(id=post_id)
    functions = {
        Post.PostTypeEnum.TEXT: send_text_message,
        Post.PostTypeEnum.IMAGE: send_image_message,
        Post.PostTypeEnum.VIDEO: send_video_message,
        Post.PostTypeEnum.ALBUM: send_album_message
    }
    functions[post.post_type](chat, post_id)


def send_text_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    text = refactor_text(text=post.content)
    bot.send_message(chat_id=chat, text=text, parse_mode="HTML")


def send_image_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    text = refactor_text(text=post.content)
    image = post.medias.first()
    bot.send_photo(chat_id=chat, photo=image.file, caption=text, parse_mode="HTML")


def send_video_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    text = refactor_text(text=post.content)
    video = post.medias.first()
    bot.send_video(chat_id=chat, video=video.file, caption=text, parse_mode="HTML")


def send_album_message(chat: str, post_id: int):
    post = Post.objects.get(id=post_id)
    medias = []
    for index, media in enumerate(post.medias.all()):
        caption = refactor_text(text=post.content) if index == 0 else None
        if media.media_type == "image":
            medias.append(types.InputMediaPhoto(media=media.file, caption=caption, parse_mode="HTML"))
        elif media.media_type == "video":
            medias.append(types.InputMediaVideo(media=media.file, caption=caption, parse_mode="HTML"))

    bot.send_media_group(chat_id=chat, media=medias)
