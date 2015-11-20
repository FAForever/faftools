"""
Contains marshmallow schemas for the JSON+API compatible part of the FAF api
"""
from .player_schema import PlayerSchema, RatingSchema
from .mod_schema import ModSchema
from .map_schema import MapSchema

# Increment me according to semver rules for compatibility
API_VERSION = '0.0.3'
