"""
Create pytest fixtures for UploadEntity tests.
"""

import mock
import pytest

from sheepdog.transactions.entity_base import EntityErrors

from tests.models import models
from tests.transactions.upload import utils


@pytest.fixture
def patch_entity_method(monkeypatch):
    """
    Provide a function which patches an ``UploadEntity`` method to use a
    different function. If the patch is used without specifying a new function
    to use, default to a ``mock.MagicMock``.

    Return:
        Callable: function to monkeypatch an UploadEntity method
    """

    def apply_patch(method_name, new_method=None):
        """
        Monkeypatch an ``UploadEntity`` method.

        Args:
            monkeypatch: the monkeypatch instance (from pytest)
            method_name (str): name of the method to patch
            new_method (Callable):
                function to patch over the method with; defaults to
                ``mock.MagicMock``

        Return:
            None

        Side Effects:
            - Patch the ``UploadEntity`` method.
        """
        new_method = new_method or mock.MagicMock(name=method_name)
        monkeypatch.setattr(utils.ENTITY_NAME + '.' + method_name, new_method)

    return apply_patch


@pytest.fixture
def entity():
    """
    Provide a basic default ``UploadEntity`` instance test fixture.

    Return:
        UploadEntity
    """
    return utils.make_new_entity()


@pytest.fixture
def transaction():
    """
    Provide a default ``mock.MagicMock`` of an ``UploadTransaction``.

    Return:
        mock.MagicMock
    """
    return utils.make_mock_transaction()


@pytest.fixture
def entity_with_error():
    """
    Provide a basic ``UploadEntity`` which has already recorded a generic
    error.

    Return:
        UploadEntity
    """
    new_entity = utils.make_new_entity()
    new_entity.record_error('test error', type=EntityErrors.UNCATEGORIZED)
    return new_entity


@pytest.fixture
def mock_lookup_node(monkeypatch):
    """
    Return a function that allows for monkeypatching of ``lookup_node``.

    Args:
        monkeypatch: the monkeypatch fixture from pytest

    Return:
        Callable:
            a function that takes an arbitrary return value, and mocks
            ``lookup_node`` to return that value instead
    """

    def set_lookup_node_return_value(return_value):
        mocked_lookup_node = mock.MagicMock(return_value=return_value)
        monkeypatch.setattr(
            utils.ENTITY_PATH + '.lookup_node', mocked_lookup_node
        )

    return set_lookup_node_return_value


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
def set_user_roles_none(patch_entity_method):
    """
    Cause ``UploadEntity.get_user_roles`` to return ``[]``.
    """
    patch_entity_method('get_user_roles', lambda _: [])
    return


@pytest.fixture
def set_user_roles_create(patch_entity_method):
    """
    Cause ``UploadEntity.get_user_roles`` to return ``['create']``.
    """
    patch_entity_method('get_user_roles', lambda _: ['create'])
    return


@pytest.fixture
def set_user_roles_create_update(patch_entity_method):
    """
    Cause ``UploadEntity.get_user_roles`` to return ``['create', 'update']``.
    """
    patch_entity_method('get_user_roles', lambda _: ['create', 'update'])
    return
