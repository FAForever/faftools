from marshmallow_jsonapi import Schema, fields


class BugReportTargetSchema(Schema):
    id = fields.String()
    name = fields.String()

    url = fields.String()
    branch = fields.String()
    hash = fields.String()


class BugReportSchema(Schema):
    id = fields.Integer(dump_only=True)

    target = fields.Nested(BugReportTargetSchema, required=True)
    automatic = fields.Boolean(default=False)

    title = fields.String(required=True)
    description = fields.String()

    log = fields.String()
    traceback = fields.String()
