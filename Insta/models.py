from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

from imagekit.models import ProcessedImageField

# Create your models here.

# when you do mods in models.py, do migrate again
# migrate is like apply this class to the project
# python manage.py makemigrations
# python manage.py migrate
# also register your model at admin.py otherwise it wont work

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

    # find all the UserConnection -> find all the objects underneath
    # -> filter to find the connection whose creator is me.
    def get_connections(self):
        connections = UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        followers = UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

class UserConnection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # I follow you, Create two people
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        # Give it a mark to so that creator's following list 
        # by using User1.friendship_creator_set
        related_name="friendship_creator_set")
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set")

    def __str__(self):
        return self.creator.username + ' follows ' + self.following.username
    
class Post(models.Model):
    author = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name = 'my_posts',
    )
    # models to find the img and collect the info about it
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True,
    )

    posted_on = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    def get_like_count(self):
        return self.likes.count()

    def get_comment_count(self):
        return self.comments.count()

    def get_absolute_url(self):
        # jump to helloworld page after save
        return reverse("post_detail", args=[str(self.id)])
    


class Like(models.Model):
    # ForeignKey pointed to other models
    post = models.ForeignKey(
        Post,
        # if post is deleted, post like will be deleted using on_delete 
        on_delete = models.CASCADE,
        # Post.likes can be used to see all the likes using related_names
        related_name ='likes',
        )
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
        related_name ='likes'
    )
    # unique_together means that (post, user) tuple can only show up onece
    # No double likes at the same post can exist
    class Meta:
        unique_together = ("post", "user")
    
    def __str__(self):
        return 'Like: ' + self.user.username + ' likes ' + self.post.title
    


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name = 'comments',
    )
    user = models.ForeignKey(
        InstaUser,
        on_delete = models.CASCADE,
    )
    comment = models.CharField(
        max_length = 100
    )
    posted_on = models.DateTimeField(
        auto_now_add = True, 
        editable = False
    )

    def __str__(self):
        return self.comment
    