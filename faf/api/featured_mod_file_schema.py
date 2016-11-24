from marshmallow_jsonapi import Schema, fields


class FeaturedModFileSchema(Schema):
    """
    Schema for 'featured_mod_file' type API objects.
    """

    id = fields.Str()

    version = fields.String()
    group = fields.String()
    name = fields.String()
    md5 = fields.String()
    url = fields.Url()

    class Meta:
        type_ = "featured_mod_file"
