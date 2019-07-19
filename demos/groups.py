from arghelp import Application, Group, arg

app = Application()


@app.subcommand(
    [
        arg("--verbose", "-v", action="store_true"),
        Group(
            [
                arg("-x", action="store_true", help="x mode"),
                arg("-y", action="store_true", help="y mode"),
            ],
            required=True,
        ),
    ]
)
def required(args):
    print(args)


@app.subcommand(
    [
        arg("--verbose", "-v", action="store_true"),
        Group(
            [
                arg("-x", action="store_true", help="x mode"),
                arg("-y", action="store_true", help="y mode"),
            ],
            required=False,
        ),
    ]
)
def optional(args):
    print(args)


@app.root_command(
    [
        arg("--flag", "-f", action="store_true"),
        Group(
            [
                arg("-u", action="store_true", help="x mode"),
                arg("-v", action="store_true", help="y mode"),
            ],
        ),
    ]
)
def root(args):
    if args.subcommand is None:
        app.cli.print_usage()
    else:
        print(args)


if __name__ == "__main__":
    app.main()
