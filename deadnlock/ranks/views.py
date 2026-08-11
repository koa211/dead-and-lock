from django.http import HttpResponse
from django.template import loader

from .models import Match


def index(request):
    recent_10_match_list = Match.objects.all()
    template = loader.get_template("ranks/index.html")
    context = {"recent_10_match_list": recent_10_match_list}
    return HttpResponse(template.render(context, request))


def daily(request, match_id):
    response = "Here is the result of your match %s."
    return HttpResponse(response % match_id)
