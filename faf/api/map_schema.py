from marshmallow_jsonapi import Schema, fields


class MapSchema(Schema):
    """
    Represents various map metadata
    """
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    map_type = fields.String()
    max_players = fields.Integer()
    battle_type = fields.String()
    map_size_x = fields.Float()
    map_size_y = fields.Float()
    version = fields.String(required=True)
    filename = fields.String(required=True)
    downloads = fields.Integer()
    num_draws = fields.Integer()
    times_played = fields.Integer()
    rating = fields.Float()

    class Meta:
        type_ = 'maps'
