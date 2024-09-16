from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

from user.models import CustomUser
from django.dispatch import receiver
from root.settings import EMAIL_DEFAULT_SENDER

from django.core.mail import send_mail
def pre_save_CustomUser(sender, instance, **kwargs):
    print(' A sample pre_save signal test')

pre_save.connect(pre_save_CustomUser, sender=CustomUser)

# @receiver(post_save, sender=CustomUser)
# def post_save_CustomUser(sender, instance, **kwargs):
#     print('Okay, good')

@receiver(post_save, sender=CustomUser)
def send_creation_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New CustomUser Notification'
        message = 'A new CustomUser has been added.'
        from_email = EMAIL_DEFAULT_SENDER
        recipient_list = [user.email for user in CustomUser.objects.all()]

        send_mail(subject, message, from_email, recipient_list)