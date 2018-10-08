from django.db import models
from django.utils.html import format_html


class User(models.Model):
    TYPES = (
            ("org", "organization"),
            ("user", "user"),
        )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    created = models.DateField()
    modified = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=255)
    followers = models.IntegerField()
    repos = models.IntegerField()
    score = models.FloatField()
    avatar = models.ImageField(upload_to='avatar', null=True)
    type = models.CharField(choices=TYPES, max_length=3)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.id,
                                          self.first_name,
                                          self.last_name,
                                          self.email)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def user_thumb(self):
        if self.avatar == "":
            url = ""
        else:
            url = self.avatar.url
            return format_html('<img height="50" width="50" src="{}" />'.format(url))


class Search(models.Model):
    query = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
