from arghelp import Application, arg

app = Application([
    arg("--verbose", "-v", action="store_true"),
])


@app.root_command()
def root(args):
    print("This is the root command. Congratulations!")


@app.subcommand([arg("name")])
def hello(args):
    """Say hello."""
    greeting = "Hello" if args.verbose else "Hi"
    print(f"{greeting} {args.name}")


@app.subcommand([arg("name")])
def goodbye(args):
    """Say goodbye."""
    bye = "Goodbye" if args.verbose else "Bye"
    print(f"{bye} {args.name}")


if __name__ == "__main__":
    app.main()
