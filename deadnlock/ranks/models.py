from django.db import models


# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()

    def __int__(self):
        return self.match_id


class Player(models.Model):
    player_id = models.TextField()
    player_name = models.TextField()
    player_damage = models.IntegerField()
    player_souls = models.IntegerField()
    player_side = models.TextField()

    def __str__(self):
        return "%s %s %s %s %s" % (self.player_id, self.player_name, self.player_damage, self.player_souls,
                                   self.player_side)
