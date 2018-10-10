from argparse import ArgumentParser, Namespace
from typing import List, Optional


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.

    """
    return list(name_or_flags), kwargs


# shortcut
arg = argument  # noqa


class Application(object):
    """A command-line application builder."""
    def __init__(self):
        self.cli = ArgumentParser()
        self.subparsers = self.cli.add_subparsers(dest="subcommand")

    def subcommand(self, args=[], parent=None):
        """Decorator to define a new subcommand in a sanity-preserving way.
        The function will be stored in the ``func`` variable when the parser
        parses arguments so that it can be called directly like so::

            args = cli.parse_args()
            args.func(args)

        Usage example::

            cli = Application()

            @cli.subcommand([arg("-d", help="Enable debug mode", action="store_true")])
            def subcommand(args):
                print(args)

        Then on the command line::

            $ python cli.py subcommand -d

        """
        parent = parent or self.subparsers

        def decorator(func):
            name = func.__name__.replace("_", "-")
            parser = parent.add_parser(name, description=func.__doc__)

            for arg in args:
                parser.add_argument(*arg[0], **arg[1])

            parser.set_defaults(func=func)

        return decorator

    def parse_args(self, args: Optional[List[str]] = None,
                   namespace: Optional[Namespace] = None) -> Namespace:
        """Parse and return command line arguments."""
        return self.cli.parse_args(args, namespace)

    def main(self) -> None:
        """Parse command line arguments and run a subcommand."""
        args = self.parse_args()

        if args.subcommand is None:
            self.cli.print_help()
            return

        else:
            args.func(args)
