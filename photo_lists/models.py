from django.db import models

# Create your models here.


class PhotoEmotion(models.Model):
    class Meta:
        db_table = "photos"

    photo_url = models.URLField(max_length=500)
    emotion = models.TextField()

    def __str__(self):
        return self.photo_url
