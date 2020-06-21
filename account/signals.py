from .models import Customer
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.db.models.signals import post_save

def customer_profile(sender, instance, created, **kwargs):
    if created:
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            customer, created = Customer.objects.get_or_create(
            user = instance, name = instance.username)
            customer.save()

post_save.connect(customer_profile,sender=User)