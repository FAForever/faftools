from marshmallow_jsonapi import Schema, fields


class AchievementSchema(Schema):
    """
    Schema for 'achievement' type API objects.
    """

    id = fields.Str()

    name = fields.String()
    description = fields.String()
    type = fields.String()
    total_steps = fields.Integer()
    initial_state = fields.String()
    experience_points = fields.Integer()
    revealed_icon_url = fields.String()
    unlocked_icon_url = fields.String()

    class Meta:
        type_ = "achievement"
