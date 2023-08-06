import os
from argparse import ArgumentParser

from dodo_commands import CommandError, ConfigArg, Dodo
from dodo_commands.framework.choice_picker import ChoicePicker


def _args():
    parser = ArgumentParser(description="Publish own npm packages")
    parser.add_argument("--login", action="store_true")

    # Add arguments to the parser here

    # Parse the arguments.
    args = Dodo.parse_args(parser, config_args=[])

    args.cwd = Dodo.get("/ROOT/project_dir")
    args.npm_dir = "/npm"
    args.src_sub_dirs = Dodo.get("/TSC/src_dir_map").keys()

    # Raise an error if something is not right
    if False:
        raise CommandError("Oops")

    return args


# Use safe=False if the script makes changes other than through Dodo.run
if Dodo.is_main(__name__, safe=True):
    args = _args()

    choices = []
    for src_sub_dir in args.src_sub_dirs:
        choices.append(dict(name=src_sub_dir, cid=src_sub_dir, image=src_sub_dir))

    class Picker(ChoicePicker):
        def print_choices(self, choices):
            for idx, container in enumerate(choices):
                print("%d - %s" % (idx + 1, container["name"]))

        def question(self):
            return "Select packages to publish: "

    picker = Picker(choices)
    picker.pick()

    if args.login:
        Dodo.run(["npm", "login"])

    for choice in picker.get_choices():
        src_sub_dir = choice["name"]
        src_dir = os.path.join(args.npm_dir, src_sub_dir)
        dist_dir = os.path.join(args.npm_dir, src_sub_dir, "dist")
        Dodo.run(["rm", "-rf", "./dist"], cwd=src_dir)
        Dodo.run(["./node_modules/.bin/tsc", "--outDir", "dist"], cwd=src_dir)
        Dodo.run(["yarn", "version", "--patch"], cwd=src_dir)
        Dodo.run(["cp", "LICENSE", "package.json", "README.md", "dist"], cwd=src_dir)
        Dodo.run(["npm", "publish"], cwd=dist_dir)
