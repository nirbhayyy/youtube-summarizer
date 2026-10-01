from django.db import models
from django.contrib.auth.models import User

class Summary(models.Model):
    user=models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name='summarizer')
    
    video_title=models.CharField(max_length=300)
    youtube_url=models.URLField()
    video_id=models.CharField(max_length=30)
    thumbnail_url=models.URLField()
    Summary=models.TextField()
    Summary_language=models.CharField(max_length=30,default='english')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    channel_name=models.CharField(max_length=200,blank=True)
    views=models.BigIntegerField(default=0)
    duration=models.CharField(max_length=20,blank=True)
    likes=models.BigIntegerField(default=0)
    sentiment = models.CharField(max_length=20, default="Neutral")
    positive_score = models.FloatField(default=0)
    negative_score = models.FloatField(default=0)
    neutral_score = models.FloatField(default=0)
    compound_score = models.FloatField(default=0)

    def __str__(self):
        return f"{self.video_title}-{self.user.username}"

