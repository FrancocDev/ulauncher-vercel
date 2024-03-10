"""
Vercel Extension
Provides quick access to your Vercel Projects
"""

import logging
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from vercel import Client as VercelClient, AuthenticationException, GenericException

LOGGER = logging.getLogger(__name__)


class VercelExtension(Extension):
    """ Main Extension Class """

    def __init__(self):
        LOGGER.info('init Vercel Extension')
        super(VercelExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.vercel_client = VercelClient("", LOGGER)

    def build_results_list(self, sites):
        """ Builds the result list from a list of sites """
        items = []

        for site in sites:
            name = site["name"]
            namespace = self.vercel_client.get_username()
            if 'targets' in site and 'production' in site['targets']:
                production_targets = site['targets']['production']
                if 'alias' in production_targets:
                    aliases = production_targets['alias']
                    if aliases:
                        url = aliases[0]
            
            if 'teamId' in site:
                namespace = self.vercel_client.get_team_slug()

            items.append(ExtensionResultItem(
                icon='images/vercel.png',
                name=name,
                on_enter=OpenUrlAction("https://" + url),
                on_alt_enter=OpenUrlAction("https://vercel.com/" + namespace + "/" + name)
            ))

        return items


class KeywordQueryEventListener(EventListener):
    """ Handles query events """

    def on_event(self, event, extension):
        """ Handle query event """
        items = []

        try:
            extension.vercel_client.set_access_token(
                extension.preferences['access_token'])
            if 'username' in extension.preferences:
               extension.vercel_client.set_username(
                    extension.preferences['username'])
            if 'team_slug' in extension.preferences:
                extension.vercel_client.set_team_slug(
                    extension.preferences['team_slug'])
            sites = extension.vercel_client.get_sites(event.get_argument())

            items = extension.build_results_list(sites)

        except AuthenticationException:
            items.append(
                ExtensionResultItem(
                    icon='images/vercel.png',
                    name="Authentication failed",
                    description="Please check the 'access_token' value on extension preferences",
                    on_enter=HideWindowAction()))
        except GenericException:
            items.append(
                ExtensionResultItem(
                    icon='images/vercel.png',
                    name="Error fetching information from Vercel",
                    on_enter=HideWindowAction()))
        return RenderResultListAction(items)


if __name__ == '__main__':
    VercelExtension().run()
