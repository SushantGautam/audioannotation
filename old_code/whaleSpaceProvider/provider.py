from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class WhaleSpaceAccount(ProviderAccount):
    pass


class WhaleSpaceProvider(OAuth2Provider):
    id = 'whalespaceprovider'
    name = 'My WhaleSpace OAuth2 Provider'
    account_class = WhaleSpaceAccount

    def extract_uid(self, data):
        return str(data['customer']['uid'])

    def extract_common_fields(self, data):
        return dict(username=data['primaryEmail'].replace('@', '_'),
                    email=data['primaryEmail'],
                    first_name=data['name']['givenName'],
                    last_name=data['name']['familyName'], )

    def get_default_scope(self):
        scope = ['https://whalepace.io/auth/directory/user.readonly']
        return scope


providers.registry.register(WhaleSpaceProvider)
