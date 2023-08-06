import os
from argparse import ArgumentParser

from dodo_commands import CommandError, ConfigArg, Dodo


def _args():
    parser = ArgumentParser(description="")
    args = Dodo.parse_args(parser)
    args.cwd = os.path.join(Dodo.get("/ROOT/src_dir"), "frontend")
    args.cypress = "./cypress/node_modules/.bin/cypress"
    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()
    Dodo.run(
        [
            "env",
            "CYPRESS_baseUrl=http://localhost:3000",
            args.cypress,
            "open",
            "--project",
            ".",
        ],
        cwd=args.cwd,
    )
