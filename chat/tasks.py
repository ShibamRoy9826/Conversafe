from datetime import timedelta
from django.utils import timezone
from celery import shared_task

from .models import chatRoom


@shared_task
def delete_inactive_chatrooms():
    """
    Celery task to delete inactive chatrooms (connectedUsers=0 for > 2 minutes).
    """
    two_minutes_ago = timezone.now() - timedelta(minutes=2)
    inactive_rooms = chatRoom.objects.filter(users=0, lastActive__lte=two_minutes_ago)
    inactive_rooms.delete()