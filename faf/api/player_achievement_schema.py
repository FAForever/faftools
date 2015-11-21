from marshmallow_jsonapi import Schema, fields


class PlayerAchievementSchema(Schema):
    """
    Schema for 'player_achievement' type API objects.
    """

    id = fields.Str()

    achievement_id = fields.String()
    state = fields.String()
    current_steps = fields.Integer(allow_none=True)
    create_time = fields.DateTime()
    update_time = fields.DateTime()

    class Meta:
        type_ = "player_achievement"
