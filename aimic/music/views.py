from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
import base64
import requests
from .models import Feedback



@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #log user in
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request, user_login)
                return redirect('/')
        else:
            messages.info(request, 'Password not matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def aboutus(request):
    return render(request, 'aboutus.html')

def search(request):
    return render(request, 'search.html')

def library(request):
    return render(request, 'library.html')

def search_tracks(request):
    query = request.GET.get('q', '')
    if query:
        access_token = get_spotify_access_token()
        if access_token:
            search_results = search_tracks_on_spotify(query, access_token)
            return render(request, 'search_results.html', {'tracks': search_results})
    return render(request, 'search_form.html')

def get_spotify_access_token():
    url = 'https://accounts.spotify.com/api/token'
    client_id = '44610704e5214488b5a442e4749fa811'
    client_secret = '0d72c4ba050e4630a66caceacfccfcd1'
    headers = {'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()}
    data = {'grant_type': 'client_credentials'}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def search_tracks_on_spotify(query, access_token):
    url = 'https://api.spotify.com/v1/search'
    headers = {'Authorization': 'Bearer ' + access_token}
    params = {'q': query, 'type': 'track'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        tracks_data = response.json().get('tracks', {}).get('items', [])
        tracks_info = []
        for track_data in tracks_data:
            track_info = {
                'name': track_data.get('name'),
                'artists': [artist.get('name') for artist in track_data.get('artists', [])],
                'album': track_data.get('album', {}).get('name'),
                'preview_url': track_data.get('preview_url'),
                'album_artwork': track_data.get('album', {}).get('images', [{}])[0].get('url')  # Get the first available image URL
            }
            tracks_info.append(track_info)
        return tracks_info
    return []


def feedback(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        feedback_text = request.POST['feedback_text']

        feedback_instance = Feedback.objects.create(name=name, email=email, feedback_text=feedback_text)
        messages.success(request, 'Thank you for your feedback!')
        return redirect('/')
    else:
        return render(request, 'feedback.html')