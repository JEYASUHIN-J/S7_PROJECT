from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Headline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # Generic Foreign Key to support multiple headline types
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    article = GenericForeignKey('content_type', 'object_id')
    
    # Keep original field for backward compatibility
    headline = models.ForeignKey(Headline, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 6)])  # 1-5 star rating

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.headline:
            return f'Comment by {self.user.username} on {self.headline.title}'
        elif self.article:
            return f'Comment by {self.user.username} on {getattr(self.article, "title", "Unknown")}'
        return f'Comment by {self.user.username}'

class EHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)

    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(content_type=ct, object_id=self.id)

class SHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)

    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(content_type=ct, object_id=self.id)

class PHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)

    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(content_type=ct, object_id=self.id)

class LHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)

    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(content_type=ct, object_id=self.id)

class ENHeadline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null = True, blank = True)
    url = models.TextField()
    source = models.CharField(max_length=200,null = True,blank=True)

    def __str__(self):
        return self.title
    
    @property
    def comments(self):
        ct = ContentType.objects.get_for_model(self.__class__)
        return Comment.objects.filter(content_type=ct, object_id=self.id)