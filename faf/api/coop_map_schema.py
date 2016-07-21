from marshmallow_jsonapi import Schema, fields


class CoopMapSchema(Schema):
    """
    Schema for 'coop_map' type API objects.
    """

    id = fields.Str()

    category = fields.String(required=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    version = fields.Integer(required=True)
    filename = fields.String(required=True)

    download_url = fields.Url(dump_only=True)
    thumbnail_url_small = fields.Url(dump_only=True)
    thumbnail_url_large = fields.Url(dump_only=True)

    class Meta:
        type_ = "coop_map"
