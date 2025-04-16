from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Appointment

@receiver(post_save, sender=Appointment)
def send_appointment_email(sender, instance, created, **kwargs):
    if created:
        subject = "Yeni Randevu Oluşturuldu"
        message = f"{instance.date} tarihinde saat {instance.time} için bir randevu oluşturuldu.\n\nNot: {instance.notes or '-'}"
        recipient = [instance.client.email]

        send_mail(
            subject,
            message,
            'bloxine11@gmail.com',  # settings.DEFAULT_FROM_EMAIL veya manuel
            ['onurbayirli17@gmail.com',],
            fail_silently=False
        )
