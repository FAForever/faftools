from marshmallow_jsonapi import Schema, fields

from faf.domain.bugs import BugReport, BugReportTarget


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

    def make_bugreport_target(self, **kwargs):
        return BugReportTarget(**kwargs)

    class Meta:
        type_ = 'bugreport_target'


class BugReportStatusSchema(Schema):
    """
    Represents the status of a bug report
    """
    id = fields.Int()
    bugreport = fields.String()
    status_code = fields.String()
    url = fields.String()

    create_time = fields.DateTime()

    class Meta:
        type_ = 'bugreport_status'


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

    create_time = fields.DateTime(allow_none=True)
    update_time = fields.DateTime(allow_none=True)

    def make_report(self, **kwargs):
        kwargs['target'] = BugReportTarget(**kwargs.get('target'))
        return BugReport(**kwargs)

    class Meta:
        type_ = 'bugreport'
