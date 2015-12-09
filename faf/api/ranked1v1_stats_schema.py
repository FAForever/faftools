from marshmallow_jsonapi import Schema, fields


class Ranked1v1StatsSchema(Schema):

    id = fields.String()
    rating_distribution = fields.Dict()

    class Meta:
        type_ = 'ranked1v1_stats'
