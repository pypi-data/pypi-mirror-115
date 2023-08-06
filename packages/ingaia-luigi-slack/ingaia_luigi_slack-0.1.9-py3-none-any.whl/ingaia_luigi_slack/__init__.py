from pkg_resources import get_distribution
from ingaia_luigi_slack.api import SlackBot, notify

__version__ = get_distribution('ingaia_luigi_slack').version
