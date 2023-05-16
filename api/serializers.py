from rest_framework import serializers
from matches.models import Highlight, Match

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = [ 'match_id', 'body', 'highlight_action', 'match_time']

class MatchSerializer(serializers.ModelSerializer):
    league_name = serializers.CharField(source='league.league_name', read_only=True)

    class Meta:
        model = Match
        exclude = ('match_link','league')
