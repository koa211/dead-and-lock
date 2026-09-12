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
import django

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from .models import Match, Player


def index(request):
    recent_10_match_list = Match.objects.all()
    template = loader.get_template("ranks/index.html")
    context = {"recent_10_match_list": recent_10_match_list}
    return HttpResponse(template.render(context, request))


def daily(request, match_id):
    template = loader.get_template("ranks/match_details.html")
    lobby_dict = {"match_details": get_match_sum(match_id)}
    print(repr(lobby_dict))
    # call another function that creates the data visualiation table

    return HttpResponse(template.render(lobby_dict, request))


# cache this somehow so I don't have to keep asking for it
def get_match_sum(match_id):
    url = f"https://api.deadlock-api.com/v1/matches/{match_id}/metadata"

    response = requests.get(url)
    byte_j = json.dumps(response.json(), separators=(",", ":"), indent=4)

    data = json.loads(byte_j)

    print("writing to file")
    with open(os.path.join(settings.MEDIA_ROOT, 'out.txt'), 'w') as file:
        file.write(byte_j)

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
                ply = Player(0, player_id, player_name, player_dmg, player_net, player_team, 0)
                obj_list.append(ply)

    obj_list.sort(key=lambda x: x.player_damage, reverse=True)

    # take max player damage *1.1 and that will be 100
    ceiling = max([float(x.player_damage) for x in obj_list]) * 1.1

    # loop through obj_list and update atr player_chart
    for one in obj_list:
        chart_num = (float(one.player_damage) / ceiling) * 100
        one.player_chart = chart_num

    print(obj_list)

    # somehow get the graph to appear right side of data
    # print("create graph")
    # postmortem(obj_list)

    return obj_list


"""
def postmortem(lobby_sum):
    df = pd.DataFrame([x.as_dict() for x in lobby_sum])
    print(df)
    names = [x.player_name for x in lobby_sum]
    ply_dmg = [float(x.player_damage) for x in lobby_sum]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.barh(names, ply_dmg, color="#c9b287", label="Hero Damage")
    ax.set_xlim(0, int(max(ply_dmg)) * 1.05)
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    ax.invert_yaxis()

    plt.savefig(os.path.join(os.path.dirname(__file__), 'static/media/pm.png'))

    # response = django.http.HttpResponse(content_type='image/png')
    # canvas.print_png(response)
"""


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
