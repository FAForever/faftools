from marshmallow_jsonapi import Schema, fields


class GameStatsAndGamePlayerStatsSchema(Schema):

    """
    Schema for 'game stats' joined with 'game player stats' type API objects.
    """

    # 'game stats' attributes
    id = fields.Str()
    game_name = fields.Str()
    victory_condition = fields.Str()
    start_time = fields.DateTime()
    map_name = fields.Str()
    map_id = fields.Str()
    mod_name = fields.Str()
    mod_id = fields.Str()
    host = fields.Str()
    validity = fields.Str()

    # 'game player' attributes
    game_id = fields.Str()
    player_id = fields.Str()
    login = fields.Str()
    team = fields.Int()
    faction = fields.Int()
    color = fields.Int()
    is_ai = fields.Bool()
    place = fields.Int()
    mean = fields.Float()
    deviation = fields.Float()
    score = fields.Int()
    score_time = fields.DateTime()

    class Meta:
        type_ = "game_stats"

