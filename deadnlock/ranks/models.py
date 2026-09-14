from django.db import models


# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField()

    def __int__(self):
        return self.match_id


class Player(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    player_id = models.TextField()
    player_name = models.TextField()
    player_damage = models.IntegerField()
    player_souls = models.IntegerField()
    player_side = models.TextField()
    player_chart = models.IntegerField()

    def __str__(self):
        return "%s %s %s %s %s" % (self.player_name, self.player_damage, self.player_souls,
                                   self.player_side, self.player_chart)

    def as_dict(self):
        return {
            'Side': self.player_side, 'Player': self.player_name, "Damage": self.player_damage,
            "Souls": self.player_souls, "Chartnum": self.player_chart
        }
