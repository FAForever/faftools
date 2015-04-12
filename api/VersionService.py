from .restservice import RestService

from . import SERVICE_URL

import logging
logger = logging.getLogger(__name__)

class VersionService(RestService):
    """
    Service to get available versions for mods, maps etc.

    TODO:
        - Use for setting the version of a hosted game,
          potentially within GameService
    """
    @staticmethod
    def versions_for(mod):
        """
        Get available versions for the given mod.

        :param mod: identifier for the mod, eg 'faf', 'blackops'
        :return: List of versions available of the mod
        """
        url = SERVICE_URL.VERSION + "/default/"+mod
        logger.debug("Getting default versions from: " + url)
        return RestService._get(url)

