from django.contrib import admin
from .models import Task, Comment, UserProfile


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'deadline', 'user')
    list_filter = ('status', 'priority', 'user')
    search_fields = ('title', 'description')
    ordering = ('deadline',)
    date_hierarchy = 'deadline'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'text', 'created_at')
    list_filter = ('task', 'user')
    search_fields = ('text',)
    readonly_fields = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'telegram_chat_id')
    search_fields = ('user__username', 'telegram_id')
