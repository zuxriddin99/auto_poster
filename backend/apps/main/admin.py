from django.contrib import admin
from apps.main.models import *

admin.site.register(PlannedPosts)


class PostMediaInlineAdmin(admin.StackedInline):
    model = PostMedia
    extra = 1


class PlannedPostsInlineAdmin(admin.StackedInline):
    model = PlannedPosts
    extra = 1
    filter_horizontal = (
        "chennals",
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_type', 'created_at')
    inlines = [PostMediaInlineAdmin, PlannedPostsInlineAdmin]


@admin.register(TelegramChennels)
class TelegramChennelsAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'channel_username')
