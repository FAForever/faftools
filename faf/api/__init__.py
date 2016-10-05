"""
Contains marshmallow schemas for the JSON+API compatible part of the FAF api
"""
from .leaderboards_stats_schema import LeaderboardsStatsSchema
from .achievement_schema import AchievementSchema
from .event_schema import EventSchema
from .leaderboards_schema import LeaderboardsSchema
from .player_achievement_schema import PlayerAchievementSchema
from .player_event_schema import PlayerEventSchema
from .player_schema import PlayerSchema, RatingSchema
from .mod_schema import ModSchema
from .clan_schema import ClanSchema
from .map_schema import MapSchema
from .bugreport_schema import BugReportSchema, BugReportTargetSchema

# Increment me according to semver rules for compatibility
API_VERSION = '0.2.0'

API_TYPES = {
    'player': PlayerSchema,
    'rating': RatingSchema,
    'mod': ModSchema,
    'map': MapSchema,
    'achievement': AchievementSchema,
    'player_achievement': PlayerAchievementSchema,
    'event': EventSchema,
    'player_event': PlayerEventSchema,
    'bugreport': BugReportSchema,
    'bugreport_target': BugReportTargetSchema,
    'leaderboards': LeaderboardsSchema,
    'leaderboards_stats': LeaderboardsStatsSchema
}

FAF_API_URL = 'http://api.dev.faforever.com'

from .client import ApiClient
