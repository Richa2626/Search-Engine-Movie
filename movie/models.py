from django.db import models

# Create your models here.

class Movie(models.Model):
    movie_name = models.CharField(max_length = 150, primary_key = True)
    movie_director = models.CharField(max_length = 100)
    ratings = models.FloatField()
    certificate = models.CharField(max_length = 5)
    duration = models.CharField(max_length = 10)
    genre = models.CharField(max_length = 50)
    release_date = models.CharField(max_length = 50)
    movie_image_url = models.URLField(null = True)
    movie_video_url = models.URLField(null = True)
    movie_credit_summary = models.CharField(max_length = 300, null = True)

    def __str__(self):
        return self.movie_name

class Movie_link(models.Model):
    # movie = models.ForeignKey(Movie , on_delete = models.CASCADE)
    movie = models.CharField(max_length = 150, primary_key = True)
    movie_links = models.URLField()

    def __str__(self):
        return self.movie
