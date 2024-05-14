from django.contrib import admin
from apps.main.models import *

admin.site.register(TelegramChennels)
admin.site.register(PlannedPosts)


class PostMediaInlineAdmin(admin.StackedInline):
    model = PostMedia
    extra = 1


class PlannedPostsInlineAdmin(admin.StackedInline):
    model = PlannedPosts
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_type', 'created_at')
    inlines = [PostMediaInlineAdmin, PlannedPostsInlineAdmin]


