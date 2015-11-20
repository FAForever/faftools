"""
Contains marshmallow schemas for the JSON+API compatible part of the FAF api
"""
from .player_schema import PlayerSchema, RatingSchema
from .mod_schema import ModSchema
from .map_schema import MapSchema
from .bugreport_schema import BugReportSchema, BugReportTargetSchema

# Increment me according to semver rules for compatibility
API_VERSION = '0.1.0'

API_TYPES = {
    'player': PlayerSchema,
    'rating': RatingSchema,
    'mod': ModSchema,
    'map': MapSchema,
    'bugreport': BugReportSchema,
    'bugreport_target': BugReportTargetSchema
}

FAF_API_URL = 'http://localhost:8080'

from .client import ApiClient
