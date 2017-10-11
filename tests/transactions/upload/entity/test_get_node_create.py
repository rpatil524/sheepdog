# pylint: disable=protected-access,unused-argument
"""
Test the functionality of ``sheepdog.transactions.upload.entity.UploadEntity``.
"""

import pytest

from sheepdog.transactions.entity_base import EntityErrors

from tests.transactions.upload import utils


@pytest.mark.parametrize(
    'entity',
    [
        utils.make_new_entity('foo'),
        utils.make_new_entity('bar'),
    ]
)
def test_create(entity, set_user_roles_create, mock_lookup_node):
    """
    Test that a user with create permission can create a new node.
    """
    # TODO: write test
    node = entity._get_node_create(skip_node_lookup=True)
    assert entity.action == 'create'
    assert node.node_id == entity.entity_id


@pytest.mark.parametrize(
    'entity',
    [
        utils.make_new_entity('foo'),
        utils.make_new_entity('bar'),
    ]
)
def test_no_permission(entity, set_user_roles_none):
    """
    Test that if a user does not have create permissions and tries to create a
    node, it fails and records an ``INVALID_PERMISSIONS`` error.
    """
    assert entity._get_node_create() is None
    error = entity.errors.pop()
    assert error['type'] == EntityErrors.INVALID_PERMISSIONS


@pytest.mark.parametrize(
    'entity',
    [
        utils.make_new_entity('foo'),
        utils.make_new_entity('bar'),
    ]
)
def test_already_exists(entity, set_user_roles_create_update):
    """
    Test that if a user with correct permissions tries to create a node that
    already exists, then no node is returned and the entity records a
    ``NOT_UNIQUE`` error.
    """
    # TODO
    assert entity._get_node_create() is None
    error = entity.errors.pop()
    assert error['type'] == EntityErrors.NOT_UNIQUE
