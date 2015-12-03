from marshmallow_jsonapi import Schema, fields


class GameStatsSchema(Schema):

    """
    Schema for 'game stats' type API objects.
    """

    id = fields.Str()
    game_name = fields.Str()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    game_mod = fields.Str()
    player_id = fields.Integer()
    map_id = fields.Integer()
    rating = fields.Float()
    game_mod_id = fields.Float()

    class Meta:
        type_ = "game stats"


class GamePlayerStatsSchema(Schema):

    """
    Schema for 'game player stats' type API objects.
    """

    id = fields.Str()
    playerId = fields.Int()
    team = fields.Int()
    faction = fields.Int()
    color = fields.Int()
    ai = fields.Int()
    place = fields.Int()
    mean = fields.Float()
    deviation = fields.Float()
    after_mean = fields.Float()
    after_deviation = fields.Float()
    score = fields.Int()
    score_time = fields.DateTime()

    class Meta:
        type_ = "game player stats"

