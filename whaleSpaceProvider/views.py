import requests
from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView)
from django.conf import settings

from .provider import WhaleSpaceProvider



class WhaleSpaceAdapter(OAuth2Adapter):
    provider_id = WhaleSpaceProvider.id

    # Fetched programmatically, must be reachable from container
    access_token_url = '{}/token'.format(settings.WHALE_OAUTH_SERVER_BASEURL)
    profile_url = '{}/userinfo'.format(settings.WHALE_OAUTH_SERVER_BASEURL)

    # Accessed by the user browser, must be reachable by the host
    authorize_url = '{}/authorize'.format(settings.WHALE_OAUTH_SERVER_BASEURL)

    # NOTE: trailing slashes in URLs are important, don't miss it

    def complete_login(self, request, app, token, **kwargs):
        headers = {'Authorization': 'Bearer {0}'.format(token.token),
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Host': 'api.whalespace.io'}
        resp = requests.get(self.profile_url, headers=headers)
        extra_data = resp.json()
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(WhaleSpaceAdapter)
oauth2_callback = OAuth2CallbackView.adapter_view(WhaleSpaceAdapter)
