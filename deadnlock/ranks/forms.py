from django import forms


class MatchForm(forms.Form):
    match_id = forms.IntegerField(label="Match ID")
