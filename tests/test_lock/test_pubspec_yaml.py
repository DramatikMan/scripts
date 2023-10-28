import subprocess as sp
from pathlib import Path

import pytest
import yaml

from .conftest import cwd, script_dir

script_path = script_dir.joinpath("pubspec_yaml.py").absolute()
pubspec_yaml_in_path = cwd.joinpath("asset/in.pubspec.yaml").absolute()
dart_pub_deps_in_path = cwd.joinpath("asset/in.dart.pub.deps.txt").absolute()


@pytest.mark.parametrize(
    ("arg", "expected_result_path"),
    (
        ("", cwd.joinpath("asset/out.pubspec.yaml").absolute()),
        ("--exact", cwd.joinpath("asset/out.exact.pubspec.yaml").absolute()),
    ),
)
def test_pubspec_yaml(arg: str, expected_result_path: Path) -> None:
    rv = sp.run(
        [
            "python3",
            str(script_path),
            str(pubspec_yaml_in_path),
            str(dart_pub_deps_in_path),
            arg,
        ],
        capture_output=True,
    )

    result = yaml.load(rv.stdout, Loader=yaml.Loader)

    with open(expected_result_path, "rb") as handle:
        expected_result = yaml.load(handle, Loader=yaml.Loader)

    assert result == expected_result
