from marshmallow_jsonapi import Schema, fields


class EventSchema(Schema):
    """
    Schema for 'event' type API objects.
    """

    id = fields.Str()

    image_url = fields.String()
    type = fields.String()
    name = fields.String()

    class Meta:
        type_ = "event"
