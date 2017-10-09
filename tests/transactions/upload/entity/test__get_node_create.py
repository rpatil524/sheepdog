# pylint: disable=protected-access,unused-argument
"""
Test the functionality of ``sheepdog.transactions.upload.entity.UploadEntity``.
"""

from sheepdog.transactions.entity_base import EntityErrors


def test_create(every_entity, set_user_roles_create):
    """
    Test that a user with create permission can create a new node.
    """
    # TODO: write test
    node = every_entity._get_node_create(skip_node_lookup=True)
    assert every_entity.action == 'create'
    assert node.node_id == every_entity.entity_id


def test_no_permission(every_entity, set_user_roles_none):
    """
    Test that if a user does not have create permissions and tries to
    create a node, it fails and records an ``INVALID_PERMISSIONS`` error.
    """
    assert every_entity._get_node_create() is None
    error = every_entity.errors.pop()
    assert error['type'] == EntityErrors.INVALID_PERMISSIONS


def test_already_exists(every_entity, set_user_roles_create_update):
    """
    Test that if a user with correct permissions tries to create a node that
    already exists, then no node is returned and the entity records a
    ``NOT_UNIQUE`` error.
    """
    assert every_entity._get_node_create() is None
    error = every_entity.errors.pop()
    assert error['type'] == EntityErrors.NOT_UNIQUE
