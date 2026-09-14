from django.test import TestCase
from .models import Player


# Create your tests here.
class PlayerTestCase(TestCase):
    def test_player_create(self):
        player = Player.objects.create(player_id="00001111", player_name="chud", player_damage=1, player_souls=20,
                                       player_side="AM", player_chart=1)
        self.assertEquals(player.player_id, "00001111")
        self.assertEquals(player.player_name, "chud")
        self.assertEquals(player.player_damage, 1)
        self.assertEquals(player.player_souls, 20)
        self.assertEquals(player.player_side, "AM")
        self.assertEquals(player.player_chart, 1)
