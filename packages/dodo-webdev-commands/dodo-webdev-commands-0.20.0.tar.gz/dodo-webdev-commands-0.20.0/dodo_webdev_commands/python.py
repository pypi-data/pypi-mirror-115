from dodo_commands import Dodo
from dodo_commands.framework.util import to_arg_list


def _args():
    Dodo.parser.add_argument("script")
    Dodo.parser.add_argument("script_args", nargs="?")
    args = Dodo.parse_args()
    args.python = Dodo.get_config("/PYTHON/python")
    args.cwd = Dodo.get_config("/PYTHON/cwd")
    return args


if Dodo.is_main(__name__):
    args = _args()
    Dodo.run([args.python, args.script, *to_arg_list(args.script_args)], cwd=args.cwd)
