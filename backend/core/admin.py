from django.contrib import admin

from .models import ChatUser, ChatMessage


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'font_color', 'created_at']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    pass
