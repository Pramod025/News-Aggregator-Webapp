from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to = "images/")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('view_article', kwargs={'title': self.title})
    
class Headline(models.Model):
  title = models.CharField(max_length=300)
  image = models.URLField(null=True, blank=True)
  url = models.TextField()
  # publishedAt = models.CharField(max_length=100, default='default_value')  # Adjust max_length and default value
  def __str__(self):
    return f"{self.title}"
