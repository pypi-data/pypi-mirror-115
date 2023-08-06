from dodo_commands import Dodo
from dodo_commands.framework.util import to_arg_list


def _args():
    Dodo.parser.description = "Run a django-manage command."
    Dodo.parser.add_argument(
        "--name",
    )
    Dodo.parser.add_argument("manage_args", nargs="?")
    args = Dodo.parse_args()
    args.python = Dodo.get_config("/DJANGO/python")
    args.cwd = Dodo.get_config("/DJANGO/cwd")
    args.manage_py = Dodo.get_config("/DJANGO/manage_py", "manage.py")
    return args


if Dodo.is_main(__name__):
    args = _args()
    if args.name:
        Dodo.get_config("/DOCKER").setdefault("options", {}).setdefault(
            "django-manage", {}
        ).setdefault("name", args.name)

    Dodo.run(
        [*to_arg_list(args.python), args.manage_py, *to_arg_list(args.manage_args)],
        cwd=args.cwd,
    )
