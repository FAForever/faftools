from marshmallow_jsonapi import Schema, fields


class LeaderboardsStatsSchema(Schema):

    id = fields.String()
    rating_distribution = fields.Dict()

    class Meta:
        type_ = 'leaderboards_stats'
