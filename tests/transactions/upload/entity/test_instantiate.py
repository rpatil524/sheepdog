import pytest

from sheepdog.transactions.upload.entity import UploadEntity

from tests.transactions.upload import utils


@pytest.mark.parametrize(
    'entity',
    [
        utils.make_new_entity('foo'),
        utils.make_new_entity('bar'),
    ]
)
def test_create(entity, set_user_roles_create, patch_entity_method):
    """
    TODO: Docstring for test_create.
    """
    # TODO: actually produce a node
    patch_entity_method('_get_node_create')
    entity.instantiate()
    UploadEntity._get_node_create.assert_called_once()
    assert entity.node


def test_attempt_create_with_errors(entity_with_error, set_user_roles_create):
    """
    Test that an entity which has encountered errors cannot instantiate its
    node.
    """
    entity_with_error.instantiate()
    assert not entity_with_error.node


@pytest.mark.parametrize(
    'entity',
    [
        utils.make_new_entity('foo', transaction_role='update'),
        utils.make_new_entity('bar', transaction_role='update'),
    ]
)
def test_update(entity, set_user_roles_create_update, patch_entity_method):
    """
    TODO
    """
    # TODO: actually produce a node
    patch_entity_method('_get_node_merge')
    entity.instantiate()
    UploadEntity._get_node_merge.assert_called_once()
    assert entity.node


def test_invalid_role(entity, set_user_roles_create):
    """
    Test that an entity with an invalid role cannot instantiate and records an
    error.
    """
    entity.transaction.role = 'garbage'
    entity.instantiate()
    assert entity.errors
