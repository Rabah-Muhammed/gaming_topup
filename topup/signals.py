from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentTransaction

@receiver(post_save, sender=PaymentTransaction)
def update_order_status(sender, instance, **kwargs):
    order = instance.topup_order
    if order.status != instance.status:
        order.status = instance.status
        order.save()
