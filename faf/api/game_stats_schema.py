from marshmallow_jsonapi import Schema, fields


class GameStatsSchema(Schema):

    """
    Schema for 'game stats' type API objects.
    """

    id = fields.Str()
    game_name = fields.Str()
    victory_condition = fields.Str()
    start_time = fields.DateTime()
    game_mod = fields.Str()
    player_id = fields.Str()
    map_id = fields.Str()
    host = fields.Str()
    validity = fields.Str()

    class Meta:
        type_ = "game_stats"


class GamePlayerStatsSchema(Schema):

    """
    Schema for 'game player stats' type API objects.
    """

    id = fields.Str()
    game_id = fields.Str()
    player_id = fields.Str()
    login = fields.Str()
    team = fields.Int()
    faction = fields.Int()
    color = fields.Int()
    has_ai = fields.Bool()
    place = fields.Int()
    mean = fields.Float()
    deviation = fields.Float()
    score = fields.Int()
    score_time = fields.DateTime()

    class Meta:
        type_ = "game_player_stats"

