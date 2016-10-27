from marshmallow_jsonapi import Schema, fields


class CoopLeaderboardSchema(Schema):
    """
    Schema for 'coop_leaderboard' type API objects.
    """

    id = fields.Integer()

    ranking = fields.Integer()
    player_names = fields.Str()
    secondary_objectives = fields.Bool()
    duration = fields.Integer()

    class Meta:
        type_ = "coop_leaderboard"
