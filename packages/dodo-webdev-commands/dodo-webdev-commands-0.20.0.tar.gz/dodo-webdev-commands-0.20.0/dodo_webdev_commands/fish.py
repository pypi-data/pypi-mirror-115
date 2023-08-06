from argparse import ArgumentParser

from dodo_commands import CommandError, ConfigArg, Dodo


def _args():
    # Create the parser
    parser = ArgumentParser(description="")
    parser.add_argument("--functions", action="store_true")

    # Use the parser to create the command arguments
    args = Dodo.parse_args(parser, config_args=[])
    args.cwd = Dodo.get("/ROOT/project_dir")

    # Raise an error if something is not right
    if False:
        raise CommandError("Oops")

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()
    if args.functions:
        print("~/.config/fish/functions")
