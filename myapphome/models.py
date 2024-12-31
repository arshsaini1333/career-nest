from django.db import models
from djongo import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return self.name

class Company(models.Model):
    companyname = models.CharField(max_length=100)
    print("companyname",companyname)
    hr_name = models.CharField(max_length=100)
    print("hr name",hr_name)
    hr_email_id = models.EmailField()
    print("hr email",hr_email_id)
    linkdin_link = models.CharField(max_length=100)
    print("linkdin link",linkdin_link)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='default-avatar.jpg')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

