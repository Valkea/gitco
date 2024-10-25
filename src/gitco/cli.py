import argparse
from .gitco import gen_commit_msg
from .utils import get_version, warn_latest


def cmd_parse():
    parser = argparse.ArgumentParser(description="Generate a commit message or display version information.")

    parser.add_argument("inspiration", nargs="?", default="", help="The idea behind the commit that the `diff` can't show")
    parser.add_argument("-v", "--version", action="store_true", help="Display current version")
    parser.add_argument("-i", "--islatest", action="store_true", help="Check if the current version is the latest")
    parser.add_argument("--debug", action="store_true", help="Display debug msg")

    # Capture all other arguments after known flags as extra_args
    parser.add_argument("git_args", nargs=argparse.REMAINDER, help="Additional git commit parameter (e.g., '-a', '-p', or '--date \"10 day ago\"')")

    # Parse known args
    args = parser.parse_args()
    return args


def app():

    args = cmd_parse()

    # Handle options
    if args.version:
        get_version()
        return
    elif args.islatest:
        warn_latest()
        return

    # Handle parameters
    flags = []
    keywords = {}

    for arg in args.git_args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            keywords[key] = value
        else:
            flags.append(arg)


    if args.debug:
        print("flags:", flags)
        print("keywords:", keywords)
        print("inspiration:", args.inspiration)

    # Call gen_commit_msg
    gen_commit_msg(args.inspiration, args.debug, *flags, **keywords)

if __name__ == "__main__":
    app()
