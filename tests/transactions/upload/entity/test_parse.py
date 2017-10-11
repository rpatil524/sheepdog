import uuid

import psqlgraph
import pytest

from sheepdog.transactions.upload.entity import UploadEntity

from tests.dictionary import dictionary


@pytest.mark.parametrize(
    'doc',
    [
        {'type': 'foo'},
        {'type': 'foo', 'id': str(uuid.uuid4())},
        {'type': 'bar'},
        {'type': 'bar', 'id': str(uuid.uuid4())},
    ]
)
def test_valid(transaction, doc):
    """
    Test that an UploadEntity initializes correctly with a given doc.

    Args:
        transaction (mock.MagicMock): pytest fixture mocking UploadTransaction
        doc (dict): the entity document to test on
    """
    transaction.role = 'create'
    entity = UploadEntity(transaction, doc)
    assert entity.doc == doc
    assert hasattr(entity, 'entity_id')
    if 'id' in doc:
        assert entity.entity_id == doc['id']
    else:
        assert entity.entity_id is None
    assert entity.entity_type == doc['type']
    cls = psqlgraph.Node.get_subclass(doc['type'])
    assert hasattr(entity, 'cls')
    assert entity.cls == cls
    assert hasattr(entity, 'category')
    assert entity.category == dictionary.schema.get(cls.label)['category']
