from argparse import Namespace
from pathlib import Path
from psenv.core.helpers import get_environment_variables, parse_config
from psenv.core.env_file import EnvFile


def inject_entrypoint(cmd: Namespace) -> None:
    config = parse_config()["environments"][cmd.env]
    path = Path(config["env"])
    env_file = EnvFile(path)
    params = get_environment_variables(cmd.prefix.upper())

    if params:
        env_file.private_content.update(**params)
        env_file.write_params_to_env(params=env_file.main_content, method="update")
        env_file.append_private_section()
    else:
        print(f"no params found in environment with prefix {cmd.prefix}")
