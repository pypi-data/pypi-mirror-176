"""Tests dict input objects for `tackle.providers.tackle.block` module."""
from tackle.main import tackle


def test_provider_tackle_flatten(change_dir):
    output = tackle('ansible.yaml', no_input=True)

    assert output


def test_provider_tackle_flatten_model():
    from tackle.providers.tackle.hooks.flatten import FlattenHook
    from tackle.models import Context

    context = Context()
    output = FlattenHook().exec()

    assert output
