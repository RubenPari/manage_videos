import google_auth_oauthlib.flow
from django.http import HttpResponse
from django.shortcuts import redirect
import os


def login(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
        redirect_uri=os.getenv('REDIRECT_URI'))

    authorization_url, state_flow = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    request.session['state'] = state_flow

    return redirect(authorization_url)


def callback(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
        state=request.session['state'],
        redirect_uri=os.getenv('REDIRECT_URI'))

    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials

    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    response = {
        'status': 'success',
        'message': 'You have successfully logged in.',
        credentials: credentials
    }

    return HttpResponse(response, status=200, content_type='application/json')
