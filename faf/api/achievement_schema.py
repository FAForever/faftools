from marshmallow_jsonapi import Schema, fields


class AchievementSchema(Schema):
    """
    Schema for 'achievement' type API objects.
    """

    id = fields.Str(dump_only=True)

    name = fields.String()
    description = fields.String()
    type = fields.String()
    total_steps = fields.Integer(allow_none=True)
    initial_state = fields.String()
    experience_points = fields.Integer()
    revealed_icon_url = fields.String(allow_none=True)
    unlocked_icon_url = fields.String(allow_none=True)

    class Meta:
        additional = ['id']
        type_ = "achievement"
