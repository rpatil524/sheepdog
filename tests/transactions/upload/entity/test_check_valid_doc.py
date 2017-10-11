import pytest

from sheepdog.transactions.entity_base import EntityErrors


# TODO: add more test cases
@pytest.mark.parametrize(
    'doc',
    [
        {'type': 'foo'},
        {'type': 'bar'},
    ]
)
def test_approve_valid(entity, doc):
    """
    Test that ``UploadTransaction._check_valid_doc`` accepts valid doc inputs.
    """
    assert entity._check_valid_doc(doc)
    assert not entity.errors


@pytest.mark.parametrize(
    'doc',
    [
        ['not', 'a', 'dictionary'],
        'still not a dictionary',
    ]
)
def test_reject_invalid_value(entity, doc):
    """
    Test that ``UploadTransaction._check_valid_doc`` rejects invalid doc
    inputs.
    """
    assert not entity._check_valid_doc(doc)
    assert entity.errors
    assert entity.errors.pop()['type'] == EntityErrors.INVALID_VALUE


@pytest.mark.parametrize(
    'doc',
    [
        {},
        {'not_type': 'foo'},
        {'type': ''},
        {'type': None},
    ]
)
def test_reject_invalid_type(entity, doc):
    """
    Test that ``UploadEntity._check_valid_doc`` rejects doc inputs that have an
    invalid or missing ``'type'`` field.
    """
    assert not entity._check_valid_doc(doc)
    assert entity.errors
    assert entity.errors.pop()['type'] == EntityErrors.INVALID_TYPE
