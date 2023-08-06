import os
from argparse import ArgumentParser

from dodo_commands import CommandError, ConfigArg, Dodo


def _args():
    parser = ArgumentParser(description="Run typescript compiler")
    parser.add_argument("src_dir_name")
    parser.add_argument("--watch", action="store_true")

    # Parse the arguments.
    args = Dodo.parse_args(parser, config_args=[])

    args.src_dir_map = Dodo.get("/TSC/src_dir_map")
    args.out_dir = Dodo.get("/TSC/out_dir", None)
    args.node_modules_dir = Dodo.get("/NODE/node_modules_dir")
    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()
    src_dir = args.src_dir_map[args.src_dir_name]
    out_dir_args = (
        ["--outDir", os.path.join(args.out_dir, os.path.basename(src_dir))]
        if args.out_dir
        else ["--outDir", "dist"]
    )
    watch_args = ["--watch"] if args.watch else []
    Dodo.run(
        [os.path.join(args.node_modules_dir, ".bin/tsc"), *watch_args, *out_dir_args],
        cwd=src_dir,
    )
