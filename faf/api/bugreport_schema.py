from marshmallow_jsonapi import Schema, fields


class BugReportTargetSchema(Schema):
    """
    Represents the target of a bug report.

    At minimum the target should have a name.

    Optionally include detailed information such as a URL describing the target,
    a branch name and a hash of the SCM revision.
    """
    id = fields.FormattedString("{name}/tree/{ref}")

    name = fields.String(required=True)

    url = fields.String()

    ref = fields.String(default='master')

    class Meta:
        type_ = 'bugreport_target'


class BugReportSchema(Schema):
    """
    Represents a generic bug report.
    """
    id = fields.String(dump_only=True)

    target = fields.Nested(BugReportTargetSchema)
    automatic = fields.Boolean(default=False)

    title = fields.String(required=True)
    description = fields.String()

    log = fields.String()
    traceback = fields.String()

    class Meta:
        type_ = 'bugreport'
