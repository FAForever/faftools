from marshmallow_jsonapi import Schema, fields


class ClanSchema(Schema):
    """
    Schema for 'clan' type API objects.
    """

    id = fields.Str()

    clan_id = fields.String(required=True)
    status = fields.Integer()
    clan_name = fields.String()
    clan_tag = fields.String()
    clan_leader_id = fields.Integer()
    clan_founder_id = fields.Integer()
    clan_desc = fields.String()
    create_date = fields.DateTime()
    leader_name = fields.String()
    founder_name = fields.String()
    clan_members = fields.Integer()

    class Meta:
        type_ = "clan"
