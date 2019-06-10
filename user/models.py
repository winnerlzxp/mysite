from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nikename = models.CharField(max_length=20, verbose_name='昵称')

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nikename, self.user.username)

def get_nikename(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nikename
    else:
        return ''

def get_nikename_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nikename
    else:
        return self.username

def has_nikename(self):
    return Profile.objects.filter(user=self).exists()

User.get_nikename = get_nikename
User.has_nikename = has_nikename
User.get_nikename_or_username = get_nikename_or_username