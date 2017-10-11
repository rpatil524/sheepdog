"""
Define utilities and constants for ``sheepdog.transactions.upload`` tests.
"""

import uuid

import mock

from sheepdog.transactions import upload


ENTITY_PATH = 'sheepdog.transactions.upload.entity'
ENTITY_NAME = 'sheepdog.transactions.upload.entity.UploadEntity'


def make_mock_transaction():
    """
    Return a mocked UploadTransaction instance.

    Return:
        mock.mock.MagicMock: a magic mock of an UploadTransaction
    """
    result = mock.create_autospec(upload.transaction.UploadTransaction)
    result.project_id = 'program-project'
    result.logger = mock.MagicMock()
    result.db_driver = mock.MagicMock()
    result.signpost = mock.MagicMock()
    return result


def make_new_entity(
        entity_type='foo', transaction_role='create', doc=None, errored=False):
    """
    Produce a new ``UploadEntity``. If the entity document is not provided
    for initialization, make a basic one with the given type and a new
    UUID.

    Args:
        entity_type (str):
            the type to give to the new entity; using examples from the GDC
            data model, this could be 'experiment' or 'case'

    Return:
        UploadEntity: the new entity with given type
    """
    new_transaction = make_mock_transaction()
    new_transaction.role = transaction_role
    doc = doc or {'type': entity_type, 'id': str(uuid.uuid4())}
    new_entity = upload.entity.UploadEntity(new_transaction, doc)
    return new_entity
