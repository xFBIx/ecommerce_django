from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile_customer, Profile_vendor

from django.db import transaction

def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))

    return inner

#@receiver(m2m_changed, sender=User.groups.through)
#@on_transaction_commit
def create_profile(sender, instance, created, **kwargs):
    if created:
        results = sender.objects.filter(pk=1)
        for staff in results:
            print(instance)
            print(instance.groups.all())
        if results[0].groups.all()[0].name == 'Customer' :
            Profile_customer.objects.create(user=instance)
            print('cr c')
        elif results[0].groups.all()[0].name == 'Vendor' :
            Profile_vendor.objects.create(user=instance)
            print('cr v')

#@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    results = sender.objects.filter(pk=1)
    if results[0].groups.all()[0].name == 'Customer' :
        instance.profile_customer.save()
        print('sv c')
    elif results[0].groups.all()[0].name == 'Vendor' :
        instance.profile_vendor.save()
        print('sv v')
