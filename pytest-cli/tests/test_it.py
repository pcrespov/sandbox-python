from pathlib import Path


def test_minimal_folder_layout(target_dir: Path):
    assert target_dir.exists()

    # has osparc folder
    assert any(target_dir.glob(".osparc/**/metadata.yml"))

    # has validation folder # TODO: define path in .osparc??
    assert (target_dir / "validation").exists()
    assert (target_dir / "validation" / "input").exists()
    assert (target_dir / "validation" / "output").exists()
