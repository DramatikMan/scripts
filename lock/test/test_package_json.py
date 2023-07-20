import json
import subprocess as sp
from pathlib import Path

import pytest

cwd = Path(__file__).parent
script_path = cwd.parent.joinpath("package_json.py").absolute()
package_json_in_path = cwd.joinpath("asset/in.package.json").absolute()
npm_list_in_path = cwd.joinpath("asset/in.npm_list.txt").absolute()


@pytest.mark.parametrize(
    ("arg", "expected_result_path"),
    (
        ("", cwd.joinpath("asset/out.package.json").absolute()),
        ("--exact", cwd.joinpath("asset/out.exact.package.json").absolute()),
    ),
)
def test_package_json(arg: str, expected_result_path: Path) -> None:
    rv = sp.run(
        [
            "python3",
            str(script_path),
            str(package_json_in_path),
            str(npm_list_in_path),
            arg,
        ],
        capture_output=True,
    )

    result = json.loads(rv.stdout)

    with open(expected_result_path, "rb") as handle:
        expected_result = json.load(handle)

    assert result == expected_result
