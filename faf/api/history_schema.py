from marshmallow_jsonapi import Schema, fields


class HistorySchema(Schema):
    """
    Represents a generic history of data.
    """
    id = fields.String()
    history = fields.Dict()

    class Meta:
        type_ = 'history'
