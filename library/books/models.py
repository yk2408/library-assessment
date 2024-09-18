from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    description = models.TextField()
    published_date = models.DateField()
    favorites = models.ManyToManyField(User, related_name='favorite_books', null=True, blank=True)

    def __str__(self):
        return self.title
