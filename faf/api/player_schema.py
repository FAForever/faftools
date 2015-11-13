from marshmallow_jsonapi import Schema, fields


class RatingSchema(Schema):
    id = fields.Int(dump_only=True)
    mean = fields.Float()
    deviation = fields.Float()


class PlayerSchema(Schema):
    id = fields.Int(dump_only=True)
    login = fields.Str()
    avatar = fields.Url()
    global_rating = fields.Nested(RatingSchema)
    ladder_rating = fields.Nested(RatingSchema)

    clan = fields.Relationship(
        '/clans/{clan_id}',
        related_url_kwargs={'clan_id': "<id>"},
        include_data=False,
        type_="clan"
    )

    class Meta:
        type_ = 'player'
