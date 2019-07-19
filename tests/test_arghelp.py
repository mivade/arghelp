import pytest

from arghelp import Application, argument, arg, Group


@pytest.fixture
def app():
    yield Application()


@pytest.mark.parametrize("func", [argument, arg])
def test_argument(func):
    args, kwargs = func(1, 2, 3, name="name")
    assert args == [1, 2, 3]
    assert kwargs == {"name": "name"}


def test_no_subcommands():
    app = Application([arg("--list", "-l", action="store_true")])
    args = app.parse_args(["-l"])
    assert args.list


def test_subcommand(app):
    @app.subcommand([arg("-x")])
    def sub1(args):
        print(args)

    @app.subcommand(([Group([arg("-x"), arg("-y")])]))
    def sub2(args):
        print(args)

    args = app.parse_args(["sub1", "-x", "1"])
    assert args.x == "1"
    args = app.parse_args(["sub2", "-y", "2"])
    assert args.y == "2"


class TestMain:
    one = False
    two = False
    root = False

    @pytest.mark.parametrize("subcommand", ["one", "two"])
    def test_multiple_subcommands(self, app, subcommand):
        @app.subcommand()
        def one(_):
            self.one = True

        @app.subcommand()
        def two(_):
            self.two = True

        app.main(args=[subcommand])

        if subcommand == "one":
            assert self.one
            assert not self.two
        else:
            assert self.two
            assert not self.one

    def test_no_subcommands(self, app):
        @app.root_command()
        def main(_):
            self.root = True

        app.main([])

        assert self.root

    @pytest.mark.parametrize("args", [[], ["one"]])
    def test_root_and_subcommand(self, app, args):
        @app.root_command()
        def main(_):
            self.root = True

        @app.subcommand()
        def one(_):
            self.one = True

        app.main(args)

        if len(args):
            assert self.one
            assert not self.root
        else:
            assert self.root
            assert not self.one
