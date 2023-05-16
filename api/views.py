from django.shortcuts import get_object_or_404,render
from django.http import StreamingHttpResponse
from django.contrib.auth import authenticate

from django.utils import timezone

from thesis_api.settings import SECRET_KEY

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


from matches.models import Match, Highlight
from users.models import UserMatch
from .serializers import HighlightSerializer, MatchSerializer
from users.serializers import RegisterUserSerializer
import uuid
import datetime
import jwt
from thesis_api.utils import jwt_auth_needed, jwt_staff_auth_needed
import requests

import json 
from django.http import JsonResponse
from django.contrib import messages



from django.contrib.auth.decorators import login_required


@login_required
def register_for_match(request):
    if request.method == 'POST':
        try:
            requestData = json.loads(request.body)
        except json.JSONDecodeError:
            JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user_id = str(request.user.id).replace('-', '')
        match_id = requestData['match_id']

        try:
            match = Match.objects.get(match_id=match_id)
        except Match.DoesNotExist:
            return JsonResponse({"error": "Invalid match_id"}, status=status.HTTP_400_BAD_REQUEST)

        user_match = UserMatch(match=match, user_id=user_id)
        try:
            user_match.save()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        messages.success(request, "Registration Sucessful.")
        return JsonResponse({"success": "Match registered successfully"}, status=status.HTTP_201_CREATED)
        
    else:
        return render(request, 'home', {})

'''
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.success(
                request, " Incorrect login details. Please try again or contact support.")
            return redirect('login')

    else:
        return render(request, 'authenticate/login.html', {})

'''





@api_view(['POST'])
def login_user_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'error': 'Please provide both email and password'})

    user = authenticate(request, email=email, password=password)

    if not user:
        return Response({'error': 'Invalid credentials'})

    payload = {
        'id': str(user.id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    # decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    return response


@api_view(['POST'])
def register_user_view(request):
    serializer = RegisterUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    response = Response({
        'email': user.email,
        'company_name': user.company_name,
        'address': user.address,
        'phone_number': user.phone_number,
        'target_link': user.target_link,
    })

    payload = {
        'id': str(user.id),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    response.set_cookie(key='jwt', value=token, httponly=True)
    return response






'''
@api_view(['POST'])
@jwt_auth_needed
def register_for_match(request):
    token = request.COOKIES.get('jwt')
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_id = decoded_token['id']    
   
    match_id = request.data['match_id'].replace('-', '')
    try:
        match = Match.objects.get(match_id=match_id)
    except Match.DoesNotExist:
        return Response({"error": "Invalid match_id"}, status=status.HTTP_400_BAD_REQUEST)

    user_match = UserMatch(match=match, user_id=user_id)
    try:
        user_match.save()
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"success": "Match registered successfully"}, status=status.HTTP_201_CREATED)

'''

@api_view(['POST'])
def logout_user_view(request):
    if 'jwt' not in request.COOKIES:
        return Response({'message': 'User is already logged out'})

    response = Response({'message': 'User has been logged out'})
    response.delete_cookie('jwt')
    return response


@api_view(['POST'])
@jwt_staff_auth_needed
def start_match(request):

    match_name = request.data['match_name']
    match_date = request.data['match_date']

    if not match_name or not match_date:
        return Response({'error': 'Both match_name and match_date are required.'}, status=status.HTTP_400_BAD_REQUEST)

    match = get_object_or_404(Match, match_name=match_name, date=match_date)
    match.is_live = True
    match.save()
    print('----------------------')

    match_id = f'{match.match_id}'
    response_data = {'status': 'success',
                     'match_id': match_id.replace('-', '')}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_staff_auth_needed
def end_match(request):
    try:
        match_id = request.data['match_id'].replace('-', '')
    except Match.DoesNotExist:
        return Response({'error': f'Match with id {match_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if not match_id:
        return Response({'error': 'match_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

    match = get_object_or_404(Match, pk=match_id)
    match.is_live = False
    match.is_done = True
    match.save()

    response_data = {'status': 'success',
                     'message': f'Match {match_id} has ended.'}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_staff_auth_needed
def change_score(request):
    try:
        match_id = request.data['match_id']
        score = request.data['score']

    except:
        return Response({'error': 'Both match_id and score are required.'}, status=status.HTTP_400_BAD_REQUEST)

    match = get_object_or_404(Match, pk=match_id)
    match.score = score
    match.save()

    response_data = {'status': 'success',
                     'message': f'Match {match_id} score has been updated to {score}.'}
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_staff_auth_needed
def add_highlight(request):

    try:
        match_id = request.data['match_id'].replace('-', '')
        match = Match.objects.get(match_id=match_id)
    except Match.DoesNotExist:
        return Response({'error': f'Match with id {match_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = HighlightSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save(match=match) 
        user_matches = UserMatch.objects.filter(match=match)
        for user_match in user_matches:
            user = user_match.user
            target_link = user.target_link
            print('FOUND USER !!!')
            print(target_link)
            if target_link:
                try:
                    payload = {
                        'match_id': str(serializer.data['match_id']).replace('-', ''),
                        'body': serializer.data['body'], 
                        'highlight_action' : serializer.data['highlight_action'], 
                        'match_time': serializer.data['match_time']
                    }
                    response = requests.post(target_link, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
                    response.raise_for_status()
                except requests.exceptions.RequestException as e:
                    # Handle request error
                    print({'error': f'Error sending request to {target_link} for user {user.id} : {str(e)}'})
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def hamadaForTeamSpirit(request):
    print('------- HAMADA !!!!!!!!!!!!!!!!')
    print(request.data)
    return Response({'error': f'No highlights found for match with id'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@jwt_auth_needed
def get_latest_highlight(request):

    try:
        match_id = request.GET.get('match_id').replace('-', '')
        # validate UUID
        match_id = uuid.UUID(match_id)
    except (ValueError, TypeError) as e:
        return Response({'error': f'Invalid match_id: {match_id}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        latest_highlight = Highlight.objects.filter(
            match_id=match_id).latest('created_at')
        serializer = HighlightSerializer(latest_highlight)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Highlight.DoesNotExist:
        return Response({'error': f'No highlights found for match with id {match_id}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@jwt_auth_needed
def get_all_highlights(request):
    try:
        match_id = request.GET.get('match_id').replace('-', '')
        # validate UUID
        match_id = uuid.UUID(match_id)
    except (ValueError, TypeError) as e:
        return Response({'error': f'Invalid match_id: {match_id}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        highlights = Highlight.objects.filter(
            match_id=match_id).order_by('-created_at')
        serializer = HighlightSerializer(highlights, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Highlight.DoesNotExist:
        return Response({'error': f'No highlights found for match with id {match_id}'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@jwt_auth_needed
def get_all_live_premium_matches(request):
    matches = Match.objects.filter(is_live=True, is_user_uploaded=False)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_auth_needed
def get_all_live_custom_matches(request):
    matches = Match.objects.filter(
        is_live=True, is_user_uploaded=True, user_id=request.user.id)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_auth_needed
def get_all_future_premium_matches(request):
    current_time = timezone.now()
    future_matches = Match.objects.filter(
        is_user_uploaded=False, is_done=False, date__gt=current_time).order_by('date')
    serializer = MatchSerializer(future_matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_auth_needed
def get_all_future_custom_matches(request):
    current_time = timezone.now()
    future_matches = Match.objects.filter(
        is_user_uploaded=True, user_id=request.user.id, is_done=False, date__gt=current_time).order_by('date')
    serializer = MatchSerializer(future_matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_auth_needed
def get_premium_matches_happening_today(request):
    current_time = timezone.now()
    today_matches = Match.objects.filter(
        is_user_uploaded=False, is_live=False, is_done=False, date=current_time.date()).order_by('time')
    serializer = MatchSerializer(today_matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@jwt_auth_needed
def get_custom_matches_happening_today(request):
    current_time = timezone.now()
    today_matches = Match.objects.filter(is_user_uploaded=True, user_id=request.user.id,
                                         is_live=False, is_done=False, date=current_time.date()).order_by('time')
    serializer = MatchSerializer(today_matches, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@jwt_auth_needed
def get_match_info(request):
    try:
        match_id = request.data.get('match_id').replace('-', '')
        # validate UUID
        match_id = uuid.UUID(match_id)
    except (ValueError, TypeError) as e:
        return Response({'error': f'Invalid match_id: {match_id}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        match = Match.objects.get(match_id=match_id)
    except Match.DoesNotExist:
        return Response({'error': 'Match not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = MatchSerializer(match)
    return Response(serializer.data, status=status.HTTP_200_OK)
