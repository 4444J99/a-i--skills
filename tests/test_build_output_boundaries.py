"""Do not let staged builds become recursive canonical inputs."""

import pytest

import skills_install as installer


@pytest.mark.parametrize(
    "canonical",
    ["skills", "plugins", "scripts", "config", ".claude-plugin", "agents", "commands"],
)
def test_build_rejects_output_in_every_recursively_copied_input(
    tmp_path, monkeypatch, canonical
):
    source = tmp_path / "source"
    source.mkdir()
    (source / canonical).mkdir()
    output = source / canonical / "nested" / "release"

    def must_not_copy(*args, **kwargs):
        pytest.fail("Build reached copying before rejecting overlapping output")

    monkeypatch.setattr(installer, "_copy_source", must_not_copy)
    with pytest.raises(installer.InstallError, match="outside canonical"):
        installer.build_release(source, output)
    assert not output.parent.exists()
    assert list((source / canonical).iterdir()) == []
