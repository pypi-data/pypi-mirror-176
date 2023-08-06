from argparse import ArgumentParser
from . import version, fetch, push, init, show, env, validation, inject


# Add your entry points / arguments in this function.....
def parse_args():
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest="command")
    sub_parsers.required = True

    version_parser = sub_parsers.add_parser("version")
    version_parser.set_defaults(func=version.version_entrypoint, help="display the current version of psenv")

    init_parser = sub_parsers.add_parser("init")
    init_parser.set_defaults(
        func=init.init_entrypoint, help="run this command once to create the ~/.psenv directory with config."
    )

    show_parser = sub_parsers.add_parser("show")
    show_parser.set_defaults(
        func=show.show_entrypoint, help="print all the configured environments in ~/.psenv/psenv.yml to the terminal"
    )

    fetch_parser = sub_parsers.add_parser("fetch")
    fetch_parser.add_argument("-m", "--method", choices=["overwrite", "update"], default="update")
    fetch_parser.set_defaults(
        func=fetch.fetch_entrypoint, help="pull parameters from the path in parameter store and populate an .env file."
    )

    push_parser = sub_parsers.add_parser("push")
    push_parser.set_defaults(func=push.push_entrypoint)
    push_parser.add_argument(
        "-o", "--overwrite", default=False, action="store_true", help="overwrite the existing parameter store value."
    )

    env_parser = sub_parsers.add_parser("env")
    env_subparser = env_parser.add_subparsers()

    env_new_parser = env_subparser.add_parser("new")
    env_new_parser.add_argument("-f", "--file", action=validation.ValidateFileName)
    env_new_parser.set_defaults(func=env.new_entrypoint)

    env_destroy_parser = env_subparser.add_parser("destroy")
    env_destroy_parser.set_defaults(func=env.destroy_entrypoint)

    inject_parser = sub_parsers.add_parser("inject")
    inject_parser.set_defaults(func=inject.inject_entrypoint)
    inject_parser.add_argument("prefix", choices=["aws"], help="copy from local environment to .env file")

    # adding the environment flag to necessary commands
    for p in fetch_parser, push_parser, env_new_parser, env_destroy_parser, inject_parser:
        p.add_argument(
            "-e",
            "--env",
            required=True,
            action=validation.ValidateEnvironmentName,
            help="name of the configured environment",
        )

    # adding the path flag to necessary commands
    for p in env_new_parser, env_destroy_parser:
        p.add_argument("-p", "--path", action=validation.ValidatePathName, help="variable path in the parameter store")

    return parser.parse_args()
