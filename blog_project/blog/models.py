from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Tale(models.Model):
    number = models.CharField(max_length=4)
    title = models.CharField(max_length=100)
    abstract = models.TextField()
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("tale-detail", kwargs={"pk": self.pk})
    


