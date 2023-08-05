"""DNS Authenticator for Online DNS."""
import logging
from typing import Optional

from lexicon.providers import online
import zope.interface

from certbot import errors
from certbot import interfaces
from certbot.plugins import dns_common
from certbot.plugins import dns_common_lexicon
from certbot.plugins.dns_common import CredentialsConfiguration

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for Online

    This Authenticator uses the Online API to fulfill a dns-01 challenge.
    """

    description = 'Obtain certificates using a DNS TXT record (if you are using Online for DNS).'
    ttl = 60

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.credentials: Optional[CredentialsConfiguration] = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super().add_parser_arguments(add, default_propagation_seconds=30)
        add('credentials', help='Online credentials INI file.')

    def more_info(self):  # pylint: disable=missing-function-docstring
        return 'This plugin configures a DNS TXT record to respond to a dns-01 challenge using ' + \
               'the Online API.'

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            'credentials',
            'Online credentials INI file',
            {
                'token': 'Private API Key for Online',
            }
        )

    def _perform(self, domain, validation_name, validation):
        client = self._get_online_client()
        client.provider.domain_id = ".".join(domain.split(".")[-2:])
        client.add_txt_record(domain, validation_name, validation)

    def _cleanup(self, domain, validation_name, validation):
        client = self._get_online_client()
        client.provider.domain_id = ".".join(domain.split(".")[-2:])
        client.del_txt_record(domain, validation_name, validation)

    def _get_online_client(self):
        if not self.credentials:  # pragma: no cover
            raise errors.Error("Plugin has not been prepared.")
        return _OnlineLexiconClient(
            self.credentials.conf('token'),
            self.ttl
        )


class _OnlineLexiconClient(dns_common_lexicon.LexiconClient):
    """
    Encapsulates all communication with the Online API via Lexicon.
    """

    def __init__(self, token, ttl):
        super().__init__()

        config = dns_common_lexicon.build_lexicon_config('online', {
            'ttl': ttl,
        }, {
            'auth_token': token,
        })

        self.provider = online.Provider(config)

    def _handle_http_error(self, e, domain_name):
        hint = None
        if str(e).startswith('400 Client Error:'):
            hint = 'Is your Application Secret value correct?'
        if str(e).startswith('403 Client Error:'):
            hint = 'Are your Application Key and Consumer Key values correct?'

        return errors.PluginError('Error determining zone identifier for {0}: {1}.{2}'
                                  .format(domain_name, e, ' ({0})'.format(hint) if hint else ''))

    def _handle_general_error(self, e, domain_name):
        if domain_name in str(e) and str(e).endswith('not found'):
            return

        super()._handle_general_error(e, domain_name)


if __name__ == '__main__':
    client = _OnlineLexiconClient("c90b654a895384470e8b94f87abcb6e9b3926d6a", 30)
    client.provider.domain_id = "s4hana.me"
    client._find_domain_id("dc1.s4hana.me")
    print(client.provider.domain)