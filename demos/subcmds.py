from arghelp import Application, arg

app = Application([arg("--verbose", "-v", action="store_true")])


@app.subcommand([arg("name")])
def hello(args):
    output = f"Hello, {args.name}!"

    if args.verbose:
        output += " How are you today?"

    print(output)


@app.subcommand([arg("name")])
def hi(args):
    output = f"Hi, {args.name}!"

    if args.verbose:
        output += " Hi hi hi!"

    print(output)


app.main()
