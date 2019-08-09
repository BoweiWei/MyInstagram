from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from imagekit.models import ProcessedImageField

# Create your models here.
class Post(models.Model):
    # models to find the img and collect the info about it
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        # jump to helloworld page after save
        return reverse("post_detail", args=[str(self.id)])
    
# when you do mods in models.py, do migrate again
# migrate is like apply this class to the project
# python manage.py makemigrations
# python manage.py migrate

# AbstractUser is the basic version of User model, add extra to 
# to create your custumized User model
class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format='JPEG',
        options={'quality': 100},
        blank=True,
        null=True,
    )