from argparse import ArgumentParser, Namespace
from typing import Callable, List, NamedTuple, Optional


Argument = NamedTuple("Argument", [
    ("name_or_flags", List[str]),
    ("kwargs", dict),
])


def argument(*name_or_flags, **kwargs) -> Argument:
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.

    """
    return Argument(list(name_or_flags), kwargs)


# shortcut
arg = argument  # noqa


class Application(object):
    """A command-line application builder.

    :param args: Common command-line arguments

    """
    def __init__(self, args: Optional[List[Argument]] = None):
        self.cli = ArgumentParser()
        self.subparsers = None
        self._root_command = None  # type: Optional[Callable]

        if args is not None:
            for arg in args:
                self.cli.add_argument(*arg.name_or_flags, **arg.kwargs)

    @property
    def subcommand_count(self) -> int:
        """Returns the number of registered subcommands."""
        if self.subparsers is not None:
            return len(self.subparsers.choices)

        return 0

    def subcommand(self, args: Optional[List[Argument]] = None):
        """Decorator to define a new subcommand in a sanity-preserving way.

        Usage example::

            app = Application()

            @app.subcommand([
                arg("-d", help="Enable debug mode", action="store_true"),
            ])
            def subcommand(args):
                print(args)

        Then on the command line::

            $ python cli.py subcommand -d

        """
        if self.subparsers is None:
            self.subparsers = self.cli.add_subparsers(dest="subcommand")

        def decorator(func):
            name = func.__name__.replace("_", "-")
            parser = self.subparsers.add_parser(name, description=func.__doc__)

            if args is not None:
                for arg in args:
                    parser.add_argument(*arg.name_or_flags, **arg.kwargs)

            parser.set_defaults(_default_func=func)

        return decorator

    def root_command(self, args: Optional[List[Argument]] = None):
        """Decorator to define the default action to take if no subcommands
        are given. The action must be a function taking a single argument which
        is the :class:`Namespace` object resulting from parsed options.

        :param args: Additional arguments to supply to the root command. Note
            that this is in addition to any common arguments supplied upon
            instantiation.

        """
        def decorator(func):
            if self._root_command is not None:
                raise RuntimeError("Only one root command can be defined")

            if args is not None:
                for arg in args:
                    self.cli.add_argument(*arg.name_or_flags, **arg.kwargs)

            self._root_command = func

        return decorator

    def parse_args(self, args: Optional[List[str]] = None,
                   namespace: Optional[Namespace] = None) -> Namespace:
        """Parse and return command line arguments."""
        return self.cli.parse_args(args, namespace)

    def main(self, args: Optional[List[str]] = None) -> None:
        """Parse command line arguments and run a subcommand."""
        args = self.parse_args(args=args)

        if self.subparsers is None:
            self._root_command(args)
            return

        if args.subcommand is None:
            if self._root_command is not None:
                self._root_command(args)
                return
            else:
                self.cli.print_help()
                return
        else:
            args._default_func(args)
