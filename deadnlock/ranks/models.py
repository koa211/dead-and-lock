from django.db import models

# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()

    def __str__(self):
        return self.match_id

