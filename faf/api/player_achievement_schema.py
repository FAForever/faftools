from marshmallow_jsonapi import Schema, fields


class PlayerAchievementSchema(Schema):
    """
    Schema for 'achievement' type API objects.
    """

    id = fields.Str()

    achievement_id = fields.String()
    state = fields.String()
    current_steps = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()

    class Meta:
        type_ = "player_achievement"
