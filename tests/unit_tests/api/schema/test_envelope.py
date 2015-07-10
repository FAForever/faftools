import marshmallow
from marshmallow import fields

from faftools.api.schema.envelope import APIDocumentSchema, BaseResource, WrappedResourceSchema


class Test:
    type = 'test'

    def __init__(self, id=None, email='example@example.com'):
        self.id = id
        self.email = email

    def __eq__(self, other):
        if not hasattr(self, 'id') or not hasattr(other, 'id'):
            return False
        if self.id is None or other.id is None:
            return False
        return self.id == other.id

    def __hash__(self):
        if not hasattr(self, 'id'):
            return 0
        else:
            return self.id.__hash__()

    def __repr__(self):
        return "Test({}, {})".format(self.id, self.email)


class TestSchema(BaseResource):
    email = fields.Email()

    class Meta:
        type = 'test'

    def make_object(self, data):
        return Test(**data)

marshmallow.class_registry.register('test', TestSchema)


def test_testschema():
    result, errors = TestSchema().load({'email': 'example2@faforever.com', 'id': '2', 'type': 'test'})
    assert result == Test('2', 'example2@faforever.com')


def test_resource_envelope_reflexive():
    schema = WrappedResourceSchema()
    tests = [Test('1', 'example1@faforever.com'), Test('2', 'example2@faforever.com')]
    dump, errors = schema.dump(tests, many=True)
    overall_result, overall_errors = schema.load(dump, many=True)
    for result, errors in overall_result:
        assert result in tests


def test_resource_envelope_fields():
    schema = WrappedResourceSchema()
    test_document = Test('1', 'example@example.com')
    dump, errors = schema.dump(test_document)

    assert dump['id'] == '1'
    assert dump['type'] == 'test'
    assert dump['attributes']['email'] == 'example@example.com'


def test_apirequest_envelope():
    schema = APIDocumentSchema()
    test_document = {
        'data': [
            Test(1, 'example@example.com')
        ]
    }
    dump, errors = schema.dump(test_document)

    assert 'data' in dump
    for item in dump['data']:
        assert 'type' in item
