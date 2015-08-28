from marshmallow import fields

class MapField(fields.Field):
    def __init__(self, from_cls, to_cls, **kwargs):
        super(MapField, self).__init__(**kwargs)
        self.from_cls = from_cls
        self.to_cls = to_cls

    def _serialize(self, value, attr, obj):
        return {self.from_cls.serialize(k, attr, obj):
                    self.to_cls.serialize(v, attr, obj) for k, v in value.items()}

    def _deserialize(self, value):
        return {self.from_cls.deserialize(k):
                    self.to_cls.deserialize(v) for k, v in dict(value).items()}

class ListField(fields.Field):
    def __init__(self, inner_cls, **kwargs):
        super(ListField, self).__init__(**kwargs)
        self.inner_cls = inner_cls

    def _serialize(self, value, attr, obj):
        return [self.inner_cls.serialize(val, attr, obj) for val in value]

    def _deserialize(self, value):
        return [self.inner_cls.deserialize(val) for val in value]


