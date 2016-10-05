from marshmallow_jsonapi import Schema, fields


class LeaderboardStatsSchema(Schema):

    id = fields.String()
    rating_distribution = fields.Dict()

    class Meta:
        type_ = 'leaderboard_stats'
