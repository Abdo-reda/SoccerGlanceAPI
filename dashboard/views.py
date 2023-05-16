from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from matches.models import Match
from users.models import UserMatch

# Create your views here.


@login_required
def custom_matches_dashboard(request):
    if request.user.is_staff:
        scheduled_matches = Match.objects.filter(is_user_uploaded=True)
    else:
        scheduled_matches = Match.objects.filter(
            is_user_uploaded=True, user_id=request.user.id)

    modified_matches = []
    for match in scheduled_matches:
        match_id = str(match.match_id).replace("-", "")
        modified_match = {
            'match_id': match_id,
            'team_1': match.team_1,
            'team_2': match.team_2,
            'score': match.score,
            'is_live': match.is_live,
            'league__league_name': match.league.league_name,
        }
        modified_matches.append(modified_match)



    registered_matches = UserMatch.objects.filter(user=request.user)
    registered_match_ids = [str(match.match.match_id).replace("-", "") for match in registered_matches]

    context = {
        'custom_matches': modified_matches,
        'registered_matches': registered_match_ids,

    }

    return render(request, './match/custom_matches_dashboard.html', context)


@login_required
def premium_matches_dashboard(request):

    premium_matches = Match.objects.filter(is_user_uploaded=False)

    modified_matches = []
    for match in premium_matches:
        match_id = str(match.match_id).replace("-", "")
        modified_match = {
            'match_id': match_id,
            'team_1': match.team_1,
            'team_2': match.team_2,
            'score': match.score,
            'is_live': match.is_live,
            'league__league_name': match.league.league_name,
        }
        modified_matches.append(modified_match)

    # Get registered matches for the logged-in user
    registered_matches = UserMatch.objects.filter(user=request.user)
    registered_match_ids = [str(match.match.match_id).replace("-", "") for match in registered_matches]

    context = {
        'premium_matches': modified_matches,
        'registered_matches': registered_match_ids,
    }
    print(context)

    return render(request, './match/premium_matches_dashboard.html', context)
