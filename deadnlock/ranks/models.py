from django.db import models

# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()

    def __int__(self):
        return self.match_id

