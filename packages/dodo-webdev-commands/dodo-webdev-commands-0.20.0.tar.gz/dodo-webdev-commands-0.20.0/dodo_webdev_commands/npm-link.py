import os
from argparse import ArgumentParser

from dodo_commands import CommandError, ConfigArg, Dodo


def _args():
    parser = ArgumentParser(description="Publish own npm packages")
    parser.add_argument("--unlink", action="store_true")

    # Parse the arguments.
    args = Dodo.parse_args(parser, config_args=[])
    args.dir_by_name = Dodo.get_config("/TSC/src_dir_map")
    args.node_modules_dir = Dodo.get_config("/NODE/node_modules_dir")
    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()

    action = "unlink" if args.unlink else "link"
    for dir_name, src_dir in args.dir_by_name.items():
        if action == "link":
            Dodo.run(["rm", "node_modules"], cwd=src_dir)
            Dodo.run(["ln", "-s", args.node_modules_dir, "node_modules"], cwd=src_dir)
            Dodo.run(["rm", "-rf", "./dist"], cwd=src_dir)
            Dodo.run(["./node_modules/.bin/tsc", "--outDir", "dist"], cwd=src_dir)
            Dodo.run(["cp", "package.json", "README.md", "dist"], cwd=src_dir)

        dist_dir = os.path.join(src_dir, "dist")
        Dodo.run(["yarn", action], cwd=dist_dir)
        Dodo.run(["yarn", action, dir_name], cwd=os.path.dirname(args.node_modules_dir))
