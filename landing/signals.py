from django.contrib.auth import user_logged_in, user_logged_out 
from notifications.signals import notify 
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

@receiver(user_logged_in) 
def user_signed_in(sender, user, **kwargs): 
    notify.send(user, recipient=user, verb=_("You signed in")) 

@receiver(user_logged_out) 
def user_signed_out(sender, user, **kwargs): 
    notify.send(user, recipient=user, verb=_("You signed out")) 