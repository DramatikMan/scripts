import subprocess as sp
import tempfile
from pathlib import Path

import pytest

cwd = Path(__file__).parent
script_path = cwd.parent.joinpath("pyproject_pdm.py").absolute()
pyproject_in_path = cwd.joinpath("asset/in.pyproject.pdm.toml").absolute()
pdm_list_in_path = cwd.joinpath("asset/in.pdm_list.txt").absolute()


@pytest.mark.parametrize(
    ("arg", "expected_result_path"),
    (
        ("", cwd.joinpath("asset/out.pyproject.pdm.toml").absolute()),
        ("--exact", cwd.joinpath("asset/out.exact.pyproject.pdm.toml").absolute()),
    ),
)
def test_package_json(arg: str, expected_result_path: Path) -> None:
    rv = sp.run(
        [
            "python3",
            str(script_path),
            str(pyproject_in_path),
            str(pdm_list_in_path),
            arg,
        ],
        capture_output=True,
    )

    with tempfile.TemporaryFile("w+") as temp, open(expected_result_path, "r") as handle:
        temp.write(rv.stdout.decode())
        temp.seek(0)

        for line1, line2 in zip(temp.readlines(), handle.readlines()):
            assert line1 == line2
