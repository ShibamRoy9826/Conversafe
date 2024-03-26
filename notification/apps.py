# from django.apps import AppConfig


# class NotificationConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'notification'

from django.apps import AppConfig

class NotisConfig(AppConfig): 
    name = "notifications"
    label = 'notif' 
    def ready(self): 
        try: 
            import notifications.signals 
        except ImportError: 
            pass