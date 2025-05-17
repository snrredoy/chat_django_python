from django.contrib import admin
from .models import Group, Chat
from django.utils.html import format_html, strip_tags
from django.utils.text import Truncator
from django.utils.safestring import mark_safe

# Register your models here.
@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at',)
    list_display_links = ('id', 'name')


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_text', 'sender', 'receiver', 'group', 'created_at',)
    list_display_links = ('id', 'content_text')

    def content_text(self, obj):
        if obj.content:
            content = strip_tags(obj.content).strip()
            if not content or content == '&nbsp;':
                return "No Title"
            content = Truncator(mark_safe(strip_tags(obj.content))).chars(30, truncate='...')
            return content
        return "No content"
    content_text.short_description = 'Content'
