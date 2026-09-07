import os

from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
import sys
import urllib
import json
import requests
import re

from .models import Match, Player


def index(request):
    recent_10_match_list = Match.objects.all()
    template = loader.get_template("ranks/index.html")
    context = {"recent_10_match_list": recent_10_match_list}
    return HttpResponse(template.render(context, request))


def daily(request, match_id):
    template = loader.get_template("ranks/match_details.html")
    lobby_sum = {"match_details": get_match_sum(match_id)}
    print(repr(lobby_sum))
    return HttpResponse(template.render(lobby_sum, request))


# cache this somehow so I don't have to keep asking for it
def get_match_sum(match_id):
    url = f"https://api.deadlock-api.com/v1/matches/{match_id}/metadata"

    response = requests.get(url)
    byte_j = json.dumps(response.json(), separators=(",", ":"), indent=4)

    data = json.loads(byte_j)

    print("writing to file")
    with open(os.path.join(settings.MEDIA_ROOT, 'out.txt'), 'w') as file:
        file.write(byte_j)

    # account_id = models.IntegerField()
    # account_name = models.TextField()
    # player_damage = models.IntegerField()
    # player_souls = models.IntegerField()   net_worth
    # player_side = models.TextField()

    obj_list = []
    time = None
    flag = False
    player_id = 0
    player_name = ""
    player_dmg = 0
    player_net = 0
    player_team = ""

    print("opening file to read")
    with open(os.path.join(settings.MEDIA_ROOT, 'out.txt'), 'r') as file:
        # get first instance of duration_s
        for line in file:
            if time:
                break
            if "duration_s" in line:
                time = line[21:25]

        for line in file:
            if "account_id" in line:
                player_id = ''.join(re.findall(r'\d', line))
                player_name = get_acc_name(player_id)

            if "time_stamp_s" in line and line.strip()[15:19] == time:
                flag = True

            if flag == True and "net_worth" in line:
                player_net = ''.join(re.findall(r'\d', line))

            if flag == True and "player_damage" in line:
                player_dmg = ''.join(re.findall(r'\d', line))

            if flag == True and re.findall("\\bteam\\b", line):
                if ''.join(re.findall(r'\d', line)) == '1':
                    player_team = "AM"
                else:
                    player_team = "HK"

                flag = False
                print(player_id, player_name, player_dmg, player_net, player_team)
                ply = Player(player_id, player_name, player_dmg, player_net, player_team)
                print(ply)
                obj_list.append(ply)

    # fix missing attribute
    print(obj_list[0].player_id)
    obj_list.sort(key=lambda x: x.player_damage, reverse=True)
    print(obj_list)

    return obj_list


def get_acc_name(account_id):
    url = requests.get(
        "https://api.deadlock-api.com/v1/players/steam-search",
        params={
            "search_query": account_id
        }
    )

    byte_j = json.dumps(url.json(), separators=(",", ":"), indent=4)
    data = json.loads(byte_j)
    return data[0]['personaname']
