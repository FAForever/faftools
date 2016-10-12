from marshmallow_jsonapi import Schema, fields


class LeaderboardHistorySchema(Schema):
    """
    Represents ranked1v1 metadata
    """
    id = fields.String()
    history = fields.List(fields.Dict())

    class Meta:
        type_ = 'leaderboard_history'
