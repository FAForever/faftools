from marshmallow_jsonapi import Schema, fields


class FeaturedModSchema(Schema):
    """
    Schema for 'featured_mod' type API objects.
    """

    id = fields.Str()

    technical_name = fields.String()
    display_name = fields.String()
    description = fields.String()
    visible = fields.String()
    display_order = fields.Int()
    git_url = fields.String()
    git_branch = fields.String()

    class Meta:
        type_ = "featured_mod"
