import json
import subprocess as sp
from pathlib import Path

import pytest

from .conftest import cwd, script_dir

script_path = script_dir.joinpath("package_json_pnpm.py").absolute()
package_json_in_path = cwd.joinpath("asset/in.package.pnpm.json").absolute()
pnpm_list_in_path = cwd.joinpath("asset/in.pnpm_list.txt").absolute()


@pytest.mark.parametrize(
    ("arg", "expected_result_path"),
    (
        ("", cwd.joinpath("asset/out.package.pnpm.json").absolute()),
        ("--exact", cwd.joinpath("asset/out.exact.package.pnpm.json").absolute()),
    ),
)
def test_package_json_pnpm(arg: str, expected_result_path: Path) -> None:
    rv = sp.run(
        [
            "python3",
            str(script_path),
            str(package_json_in_path),
            str(pnpm_list_in_path),
            arg,
        ],
        capture_output=True,
    )

    result = json.loads(rv.stdout)

    with open(expected_result_path, "rb") as handle:
        expected_result = json.load(handle)

    assert result == expected_result
