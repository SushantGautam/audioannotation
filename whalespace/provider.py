from allauth.account.models import EmailAddress
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class WhaleSpaceAccount(ProviderAccount):
    def get_avatar_url(self):
        return self.account.extra_data.get("thumbnailPhotoUrl")

    def to_str(self):
        return self.account.extra_data.get("fullName", self.account.uid)


class WhaleSpaceProvider(OAuth2Provider):
    id = "whalespace"
    name = "WhaleSpace"
    account_class = WhaleSpaceAccount

    def extract_uid(self, data):
        return str(data['sid'])

    def extract_common_fields(self, data):
        return dict(username=data['primaryEmail'].replace('@', '_'),
                    email=data['primaryEmail'],
                    first_name=data['name']['givenName'],
                    last_name=data['name']['familyName'])

    def extract_email_addresses(self, data):
        ret = []
        email = data.get("primaryEmail")
        if email:
            ret.append(EmailAddress(email=email, verified=True, primary=True))
        return ret


provider_classes = [WhaleSpaceProvider]