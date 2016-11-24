from marshmallow_jsonapi import Schema, fields

from faf.api import MapSchema
from faf.api.featured_mod_schema import FeaturedModSchema
from faf.api.player_schema import PlayerSchema


class ReplaySchema(Schema):
    """
    Schema for 'replay' type API objects.
    """

    id = fields.String()

    title = fields.String()

    featured_mod = fields.Relationship(
        related_url='/featured_mod/{featured_mod_id}',
        related_url_kwargs={'featured_mod_id': '<id>'},
        type_='feratured_mod',
        schema=FeaturedModSchema,
        include_resource_linkage=True
    )

    map = fields.Relationship(
        related_url='/maps/{map_id}',
        related_url_kwargs={'map_id': '<id>'},
        type_='map',
        schema=MapSchema,
        include_resource_linkage=True
    )

    players = fields.Relationship(
        related_url='/players/{player_id}',
        related_url_kwargs={'player_id': '<id>'},
        type_='player',
        schema=PlayerSchema,
        include_resource_linkage=True,
        many=True
    )

    start_time = fields.DateTime()
    end_time = fields.DateTime()
    views = fields.Integer()
    teams = fields.Dict()

    class Meta:
        type_ = "replay"
