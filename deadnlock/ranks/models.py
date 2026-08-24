from django.db import models


# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()

    def __int__(self):
        return self.match_id


class Player(models.Model):
    account_id = models.IntegerField()
    account_name = models.TextField()
    player_damage = models.IntegerField()
    player_souls = models.IntegerField()
    player_side = models.TextField()
