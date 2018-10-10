from arghelp import Application, arg

app = Application()

verbose_arg = arg("--verbose", "-v", action="store_true")


@app.subcommand([verbose_arg, arg("name")])
def hello(args):
    """Say hello."""
    greeting = "Hello" if args.verbose else "Hi"
    print(f"{greeting} {args.name}")


@app.subcommand([verbose_arg, arg("name")])
def goodbye(args):
    """Say goodbye."""
    bye = "Goodbye" if args.verbose else "Bye"
    print(f"{bye} {args.name}")


app.main()
