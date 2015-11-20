class BugReportTarget:
    def __init__(self, name, url=None, ref=None):
        self.name = name
        self.url = url
        self.ref = ref

    @property
    def id(self):
        return "{}/tree/{}".format(self.name, self.ref)


class BugReport:
    """
    Represents a bug report
    """
    def __init__(self,
                 title,
                 id=None,
                 target=BugReportTarget(name='FAForever/client'),
                 automatic=False,
                 description="",
                 log="",
                 traceback=""):
        self.title = title
        self.id = id
        self.target = target
        self.automatic = automatic
        self.description = description
        self.log = log
        self.traceback = traceback
