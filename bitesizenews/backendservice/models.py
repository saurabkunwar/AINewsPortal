from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=2000)
    content = models.TextField()
    summarization = models.TextField(blank=True, null=True)
    link = models.URLField()
    publisher = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
         return self.title