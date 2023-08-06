from dodo_commands import Dodo
from dodo_commands.framework.decorator_scope import DecoratorScope
from dodo_commands.framework.util import to_arg_list
from dodo_docker_commands.decorators.docker import invert_path


def _args():
    Dodo.parser.add_argument("yarn_args", nargs="?")
    Dodo.parser.add_argument("--name")
    Dodo.parser.add_argument("--local", "-l", action="store_true")
    args = Dodo.parse_args()
    args.yarn = "yarn"
    args.cwd = Dodo.get_config("/NODE/cwd")
    return args


if Dodo.is_main(__name__, safe=True):
    args = _args()

    if args.name:
        Dodo.get_config("/DOCKER").setdefault("options", {}).setdefault("yarn", {})[
            "name"
        ] = args.name

    if args.local:
        with DecoratorScope("docker", remove=True):
            Dodo.run(
                [args.yarn, *to_arg_list(args.yarn_args)], cwd=invert_path(args.cwd)
            )
    else:
        Dodo.run([args.yarn, *to_arg_list(args.yarn_args)], cwd=args.cwd)
