from marshmallow_jsonapi import Schema, fields


class PlayerEventSchema(Schema):
    """
    Schema for 'player_event' type API objects.
    """

    id = fields.Str(dump_only=True)

    player_id = fields.Integer()
    event_id = fields.String()
    count = fields.Integer()

    class Meta:
        type_ = "player_event"
