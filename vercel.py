"""Vercel Module"""

import requests
from cache import Cache


class Client(object):
    """CLass that interacts with Vercel API"""

    API_PROJECTS_URL = "https://api.vercel.com/v9/projects/"

    CACHE_TTL = 3600  # 1h

    CACHE_KEY = "vercel_sites"

    def __init__(self, access_token, logger):
        """ Class constructor """
        self.access_token = access_token
        self.logger = logger
        self.username = ""
        self.team_slug = ""

    def set_access_token(self, access_token):
        """ Sets the Access Token """
        self.access_token = access_token

    def set_username(self, username):
        """ Sets the Username """
        self.username = username

    def set_team_slug(self, team_slug):
        """ Sets the Team Slug """
        self.team_slug = team_slug

    def get_team_slug(self):
        """ Gets the Team Slug """
        return self.team_slug

    def get_username(self):
        """ Gets the Username """
        return self.username

    def filter_sites(self, sites, filter_term=None):
        """Filter the sites returned by Vercel, by the name passed in filter parameter"""
        if not filter_term:
            return sites

        filtered_sites = []
        for site in sites:
            production_targets = site.get('targets', {}).get('production', {})
            aliases = production_targets.get('alias', [])

            if filter_term.lower() in site['name'].lower() or (filter_term.lower() in aliases) or any(filter_term.lower() in alias.lower() for alias in aliases):
                filtered_sites.append(site)

        return filtered_sites

    def get_sites(self, filter_term=None):
        """Gets a list of user sites from Vercel"""

        self.logger.debug("getting sites from Vercel")

        if Cache.get(self.CACHE_KEY):
            self.logger.debug("Loading from cache")
            return self.filter_sites(Cache.get(self.CACHE_KEY), filter_term)

        headers = {
            "Authorization": "Bearer {}".format(
                self.access_token),
            "Accept": "application/json",
            "User-Agent": "Ulauncher-Vercel"}
        req = requests.get(self.API_PROJECTS_URL, headers=headers)

        if not req.ok:
            if req.status_code == 401:
                raise AuthenticationException(
                    "Failed to authenticate with access token " + self.access_token)

            raise GenericException(
                "Error connecting to Vercel API : status " + req.status_code)

        data = req.json()
        data = data.get('projects', [])
        Cache.set(self.CACHE_KEY, data, self.CACHE_TTL)

        return self.filter_sites(data, filter_term)

class GenericException(Exception):
    """ Generic Exception """

class AuthenticationException(Exception):
    """ Exception thrown when the Authentication on Vercel fails """
