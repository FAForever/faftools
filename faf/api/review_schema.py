from marshmallow_jsonapi import Schema, fields


class ReviewSchema(Schema):
    """
    Represents various review metadata
    """
    id = fields.Str()
    text = fields.String(required=True)
    rating = fields.Integer()
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    description = fields.String(required=True)
    user_id = fields.Integer()
    user_name = fields.String()

    class Meta:
        type_ = 'review'
