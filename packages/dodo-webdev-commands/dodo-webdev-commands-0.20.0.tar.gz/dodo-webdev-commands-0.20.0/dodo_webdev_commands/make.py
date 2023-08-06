from dodo_commands import CommandError, DecoratorScope, Dodo
from dodo_commands.framework.global_config import (global_config_get,
                                                   load_global_config_parser)
from dodo_commands.framework.util import to_arg_list
from dodo_docker_commands.decorators.docker import invert_path


def _args():
    Dodo.parser.description = "Runs make"

    Dodo.parser.add_argument("make_args", nargs="?")
    Dodo.parser.add_argument("--cat", action="store_true")
    Dodo.parser.add_argument("--edit", action="store_true")

    args = Dodo.parse_args()
    args.cwd = Dodo.get_config("/MAKE/cwd")
    args.file = Dodo.get_config("/MAKE/file", "Makefile")

    global_config = load_global_config_parser()
    args.editor = global_config_get(global_config, "settings", "editor")

    # Raise an error if something is not right
    if False:
        raise CommandError("Oops")

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()

    if args.cat:
        Dodo.run(["cat", args.file], cwd=args.cwd)
    elif args.edit:
        with DecoratorScope("docker", remove=True):
            Dodo.run([args.editor, args.file], cwd=invert_path(args.cwd))
    else:
        file_args = ["-f", args.file] if args.file != "Makefile" else []
        Dodo.run(["make", *file_args, *to_arg_list(args.make_args)], cwd=args.cwd)
