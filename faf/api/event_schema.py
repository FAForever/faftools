from marshmallow_jsonapi import Schema, fields


class EventSchema(Schema):
    """
    Schema for 'event' type API objects.
    """

    id = fields.Str()

    image_url = fields.String(allow_none=True)
    type = fields.String()
    name = fields.String()

    class Meta:
        type_ = "event"
