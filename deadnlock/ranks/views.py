import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.loader import render_to_string
from django.shortcuts import render

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
from .forms import MatchForm


def home_view(request):
    # text box, when user enters number and enter, run find match API, if 200 then call daily
    if request.method == "POST":
        form = MatchForm(request.POST)
        if form.is_valid():
            match_id = form.cleaned_data["match_id"]
            return HttpResponseRedirect(f"/ranks/{match_id}/")

    else:
        form = MatchForm()

    return render(request, "ranks/home.html", {"form": form})


def index(request):
    recent_10_match_list = Match.objects.all()
    template = loader.get_template("ranks/index.html")
    context = {"recent_10_match_list": recent_10_match_list}
    return HttpResponse(template.render(context, request))


def daily(request, match_id):
    template = loader.get_template("ranks/match_details.html")
    lobby_dict = {"match_details": get_match_sum(match_id)}
    return HttpResponse(template.render(lobby_dict, request))


# cache this somehow so I don't have to keep asking for it
def get_match_sum(match_id):
    url = f"https://api.deadlock-api.com/v1/matches/{match_id}/metadata"
    response = requests.get(url)
    data = response.json()

    duration = data["match_info"]["duration_s"]

    match_players = data["match_info"]["players"]

    obj_list = []

    for player in match_players:
        player_id = player["account_id"]
        player_name = get_acc_name(player_id)
        player_team = "AM" if player["team"] == 1 else "HK"
        player_net = player["net_worth"]

        snap = player["stats"][-1]

        ply = Player(0, player_id, player_name, snap["player_damage"], snap["net_worth"], player_team, 0)
        obj_list.append(ply)

    obj_list.sort(key=lambda x: x.player_damage, reverse=True)

    print(obj_list)

    # take max player damage *1.1 and that will be 100
    ceiling = max([float(x.player_damage) for x in obj_list]) * 1.1

    # loop through obj_list and update atr player_chart
    for one in obj_list:
        chart_num = (float(one.player_damage) / ceiling) * 100
        one.player_chart = chart_num

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
