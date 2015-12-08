from marshmallow_jsonapi import Schema, fields


class LeaderboardSchema(Schema):
    """
    Represents leaderboard metadata
    """
    id = fields.Integer()
    login = fields.String()
    mean = fields.Float()
    deviation = fields.Float()
    num_games = fields.Integer()
    won_games = fields.Integer()
    is_active = fields.Boolean()
    rating = fields.Integer()
    ranking = fields.Integer()

    class Meta:
        type_ = 'leaderboard'
