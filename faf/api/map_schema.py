from marshmallow_jsonapi import Schema, fields


class MapSchema(Schema):
    """
    Represents various map metadata
    """
    id = fields.Integer()
    display_name = fields.String(required=True)
    description = fields.String(required=True)
    version = fields.String(required=True)
    filename = fields.String(required=True)

    map_type = fields.String()
    max_players = fields.Integer()
    battle_type = fields.String()
    map_size_x = fields.Float()
    map_size_y = fields.Float()

    # Read only fields
    downloads = fields.Integer(dump_only=True)
    num_draws = fields.Integer(dump_only=True)
    times_played = fields.Integer(dump_only=True)
    rating = fields.Float(dump_only=True)
    download_url = fields.Url(dump_only=True)
    thumbnail_url_small = fields.Url(dump_only=True)
    thumbnail_url_large = fields.Url(dump_only=True)
    technical_name = fields.String(dump_only=True)

    class Meta:
        type_ = 'map'
