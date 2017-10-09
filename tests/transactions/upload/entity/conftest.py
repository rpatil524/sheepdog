# pylint: disable=redefined-outer-name
"""
Create fixtures and utility functions for UploadEntity tests.
"""

import logging
import uuid

import mock
import psqlgraph
import pytest

from sheepdog.transactions import upload
from sheepdog.transactions.upload.entity import UploadEntity

from tests.models import models


ENTITY_PATH = 'sheepdog.transactions.upload.entity'
ENTITY_NAME = 'sheepdog.transactions.upload.entity.UploadEntity'


def patch_entity_method(monkeypatch, method_name, new_method):
    """
    Monkeypatch an ``UploadEntity`` method.

    Args:
        monkeypatch: the monkeypatch instance (from pytest)
        method_name (str): name of the method to patch
        new_method (Callable):
            function to patch over the method with; assume that it will have
            the same signature as the original method

    Return:
        None

    Side Effects:
        Monkeypatch the given ``UploadEntity`` method to use the new function.
    """
    monkeypatch.setattr(ENTITY_NAME + '.' + method_name, new_method)
    return


def make_new_entity(entity_type='foo', transaction_role='create'):
    """
    Produce a new ``UploadEntity`` that has been initialized with
    ``UploadEntity.parse`` using the given entity type.

    Args:
        entity_type (TODO):
            the type to give to the new entity; using examples from the GDC
            data model, this could be 'Experiment' or 'Case'

    Return:
        UploadEntity: the new entity with given type
    """
    new_transaction = transaction()
    new_transaction.role = transaction_role
    new_entity = entity(new_transaction)
    doc = {'type': entity_type, 'id': str(uuid.uuid4())}
    new_entity.parse(doc)
    return new_entity


@pytest.fixture(autouse=True)
def mock_get_subclass(monkeypatch):
    """
    Define the mapping that will be done by ``psqlgraph.Node.get_subclass``
    from entity types as strings to the actual classes.

    NOTE that this fixture is autoused, and the mapping here is effectively
    exhaustive (if a type-to-class mapping is not listed here, then
    ``psqlgraph.Node`` is unable to look up that class).

    Args:
        monkeypatch: the monkeypatch fixture from pytest

    Return:
        None

    Side Effects:
        - Patch ``psqlgraph.Node.get_subclass`` to only follow the mapping
          defined here.
    """
    mapping = {
        'program': models.Program,
        'project': models.Project,
        'foo': models.Foo,
        'bar': models.Bar,
    }

    def side_effect(entity_type):
        return mapping[entity_type]

    mocked_get_subclass = mock.MagicMock(side_effect=side_effect)
    monkeypatch.setattr('psqlgraph.Node.get_subclass', mocked_get_subclass)


@pytest.fixture
def set_user_roles_none(monkeypatch):
    """
    Cause ``UploadEntity.get_user_roles`` to return ``[]``.
    """
    allow_none = lambda _: []  # noqa
    patch_entity_method(monkeypatch, 'get_user_roles', allow_none)
    return


@pytest.fixture
def set_user_roles_create(monkeypatch):
    """
    Cause ``UploadEntity.get_user_roles`` to return ``['create']``.
    """
    allow_create = lambda _: ['create']  # noqa
    patch_entity_method(monkeypatch, 'get_user_roles', allow_create)
    return


@pytest.fixture
def set_user_roles_create_update(monkeypatch):
    """
    Cause ``UploadEntity.get_user_roles`` to return ``['create', 'update']``.
    """
    allow_create_update = lambda _: ['create', 'update']  # noqa
    patch_entity_method(monkeypatch, 'get_user_roles', allow_create_update)
    return


@pytest.fixture
def transaction():
    """
    Return a mocked UploadTransaction instance.

    Return:
        mock.mock.MagicMock: a magic mock of an UploadTransaction
    """
    result = mock.create_autospec(upload.transaction.UploadTransaction)
    result.project_id = 'program-project'
    result.logger = logging.getLogger('UploadTransaction')
    result.db_driver = None
    result.signpost = None
    return result


@pytest.fixture
def entity(transaction):
    """
    Return a basic UploadEntity instance.

    Note that the UploadTransaction for this entity is mocked (see
    ``transaction``).

    Return:
        UploadEntity
    """
    result = UploadEntity(transaction)
    return result


# Use the ``pytest_generate_tests`` hook to set the parametrization. Here, set
# the ``every_entity`` parametrization to use all the entity test bars we want
# to run, so every test that uses the ``every_entity`` fixture will be called
# once with each entity in ``all_test_entities``.
def pytest_generate_tests(metafunc):
    """
    Define pytest hook to run when collecting a test function.
    """
    # Define the list of entities that will be used for testing.
    all_test_entities = [
        make_new_entity('foo'),
        make_new_entity('bar'),
    ]

    if 'every_entity' in metafunc.fixturenames:
        metafunc.parametrize('every_entity', all_test_entities)
