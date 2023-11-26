# by shenjackyuanjie
# 20231125
# 为啥就把 requirements.txt 删掉了 (恼)

import tomli

with open("pyproject.toml", "r", encoding="utf-8") as f:
    pyproject = tomli.loads(f.read())

with open("requirements.txt", "w", encoding="utf-8") as f:
    for dependency in pyproject["project"]["dependencies"]:
        print(dependency)
        f.write(dependency + "\n")
