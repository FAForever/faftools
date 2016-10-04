from marshmallow_jsonapi import Schema, fields


class ModSchema(Schema):
    """
    Schema for 'mods' type API objects.
    """

    id = fields.Str()

    display_name = fields.String(required=True)
    description = fields.String()
    version = fields.String()
    author = fields.String()
    downloads = fields.Integer()
    likes = fields.Integer()
    times_played = fields.Integer()
    download_url = fields.Url()
    thumbnail_url = fields.Url(allow_none=True)
    type = fields.String()
    is_ranked = fields.Boolean()
    create_time = fields.DateTime()

    class Meta:
        type_ = "mod"
