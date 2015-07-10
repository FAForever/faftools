from copy import deepcopy
import marshmallow
from marshmallow import Schema, SchemaOpts, fields
from marshmallow.decorators import pre_load, post_dump, pre_dump, post_load

RESOURCE_TYPES = {}

class BaseResource(Schema):
    id = fields.String()


class WrappedResourceSchema(BaseResource):
    """
    Envelope for JSON API compliant resource objects
    """
    type = fields.String()
    attributes = fields.Raw()
    relationships = fields.Arbitrary()
    links = fields.Arbitrary()

    @pre_load()
    def deserialize(self, data, many=False):
        type = marshmallow.utils.get_value('type', data)
        id = marshmallow.utils.get_value('id', data)
        schema = marshmallow.class_registry.get_class(type)()
        obj = {'id': id,
               'type': type}
        obj.update(data['attributes'])
        return obj

    @pre_dump()
    def serialize(self, data, many=False):
        type = getattr(data, 'type')
        id = marshmallow.utils.get_value('id', data)
        data, errors = marshmallow.class_registry.get_class(type)().dump(data, many=many)
        if 'type' in data:
            del data['type']
        if 'id' in data:
            del data['id']
        return {
            'id': id,
            'type': type,
            'attributes': data
        }

    def make_object(self, data):
        type = data['type']
        del data['type']
        return marshmallow.class_registry.get_class(type)().load(data)

class APIErrorSchema(Schema):
    pass


class APILinksSchema(Schema):
    pass


class APIDocumentSchema(Schema):
    """
    Represents a JSON API request / response document.

    See specification at http://www.jsonapi.org
    """

    data = fields.Nested(WrappedResourceSchema, many=True)
    errors = fields.Nested(APIErrorSchema, many=True)
    meta = fields.Arbitrary()

    jsonapi = fields.Arbitrary()
    included = fields.Nested(WrappedResourceSchema, many=True)
