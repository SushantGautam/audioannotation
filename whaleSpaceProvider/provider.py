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
        return str(data['id'])

    def extract_common_fields(self, data):
        return dict(username=data['username'],
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'], )

    def get_default_scope(self):
        scope = ['https%3A//whalespace.io/directory/user.profile.readonly']
        return scope


providers.registry.register(WhaleSpaceProvider)
