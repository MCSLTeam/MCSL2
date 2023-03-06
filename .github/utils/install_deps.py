import os
from pathlib import Path

from tomlkit import parse

pyproject = parse((Path.cwd() / "pyproject.toml").read_text(encoding="u8"))
deps = pyproject["tool"]["poetry"]["dependencies"]
deps.update(pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"])

if "python" in deps:
    del deps["python"]

for d, v in deps.items():
    v = f"=={v.removeprefix('^')}" if v.startswith("^") else v
    os.system(f'pip install "{d}{v}"')
