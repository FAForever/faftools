from marshmallow_jsonapi import Schema, fields


class RatingSchema(Schema):
    id = fields.Int(dump_only=True)
    mean = fields.Float()
    deviation = fields.Float()

    class Meta:
        type_ = 'rating'


class AvatarSchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.Url(required=True)
    tooltip = fields.String(required=True)

    class Meta:
        type_ = 'avatar'

class ClanSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.String(required=True)
    tag = fields.String(required=True)

    class Meta:
        type_ = 'clan'


class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    login = fields.Str()
    avatar = fields.Nested(AvatarSchema)

    global_rating = fields.Nested(RatingSchema)
    ladder_rating = fields.Nested(RatingSchema)

    clan = fields.Relationship(
        '/clans/{clan_id}',
        related_url_kwargs={'clan_id': "<id>"},
        include_data=False,
        type_='clans'
    )

    class Meta:
        type_ = 'player'
