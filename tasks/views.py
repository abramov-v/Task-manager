import logging
import requests
from django.conf import settings
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task, Comment, UserProfile
from .serializers import TaskSerializer, CommentSerializer


logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """Sends a notification via Telegram"""
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'Markdown'}

    logger.info(f" Attempting to send a message via Telegram: {data}")

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        logger.info("✅ Message successfully sent!")
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error sending Telegram message: {e}")


class TaskViewSet(viewsets.ModelViewSet):
    """API View for managing tasks"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter
                       ]
    filterset_fields = ['status', 'priority', 'user']
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'priority']
    ordering = ['deadline']

    def perform_create(self, serializer):
        """Assigns the task to the current user upon creation"""
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """API View for managing comments"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filters comments by task_id"""
        task_id = self.kwargs.get('task_id')
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        """Creates a comment and notifies the task owner via Telegram"""
        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        comment = serializer.save(user=self.request.user, task=task)

        task_owner = task.user
        profile = UserProfile.objects.filter(user=task_owner).first()

        if profile and profile.telegram_chat_id:
            message = (
                f"📝 *New comment on task:* {task.title}\n\n"
                f"👤 *From:* {self.request.user.username}\n"
                f"💬 {comment.text}"
            )
            send_telegram_message(profile.telegram_chat_id, message)
        else:
            logger.warning("❌ User does not have a Telegram Chat ID")
