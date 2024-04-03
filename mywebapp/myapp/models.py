from django.db import models


class ComicBookStore(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Webtoon(models.Model):
    name = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    rating = models.FloatField()
    english_link = models.URLField()
    english_release_date = models.DateField()
    status = models.CharField(max_length=100)
    image_url = models.URLField()
    summary = models.TextField()
