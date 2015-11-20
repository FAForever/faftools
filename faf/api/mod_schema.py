from marshmallow_jsonapi import Schema, fields


class ModSchema(Schema):
    """
    Schema for 'mods' type API objects.
    """

    id = fields.Str()

    name = fields.String(required=True)
    description = fields.String()
    version = fields.String()
    author = fields.String()
    downloads = fields.Integer()
    likes = fields.Integer()
    plays = fields.Integer()
    filename = fields.String()
    icon_filename = fields.String()
    is_ui = fields.Boolean()
    is_ranked = fields.Boolean()
    create_time = fields.DateTime()

    class Meta:
        type_ = "mod"
