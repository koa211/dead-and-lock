from django.http import HttpResponse
from django.template import loader
import sys
import json
import requests

from .models import Match


def index(request):
    recent_10_match_list = Match.objects.all()
    template = loader.get_template("ranks/index.html")
    context = {"recent_10_match_list": recent_10_match_list}
    return HttpResponse(template.render(context, request))


def daily(request, match_id):
    template = loader.get_template("ranks/match_details.html")
    # api call here
    match_details = {"match_details": get_matches(match_id)}
    return HttpResponse(template.render(match_details, request))


def get_matches(match_id):
    url = "https://api.deadlock-api.com/v1/matches/metadata"
    params = {
        'match_id': match_id,
    }

    response = requests.get(url, params=params)
    byte_j = json.dumps(response.json(), separators=(",", ":"), indent=4)

    return byte_j
