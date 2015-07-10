from marshmallow import Schema, fields, post_dump


class Message(Schema):
    data = fields.Method('serialize_data', 'deserialize_data')
    included = fields.Method('serialize_included', 'deserialize_included', allow_none=True)

    @post_dump(raw=True)
    def wrap(self, data, many):
        if 'included' in data and data['included'] is None:
            del data['included']
        return data

    def serialize_data(self, obj=None):
        if isinstance(obj, list):
            many = True
        else:
            many = False
        result, errors = self.context['schema_type'].dump(obj, many)
        return result

    def deserialize_data(self, value=None):
        if isinstance(value, list):
            many = True
        else:
            many = False
        result, errors = self.context['schema_type'].load(value, many)
        return result

    def serialize_included(self, obj=None):
        pass

    def deserialize_included(self, obj=None):
        pass
