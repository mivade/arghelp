from arghelp import Application, arg

app = Application()


@app.root_command()
def main(_):
    print("Nothing to see here. Move along!")


@app.subcommand()
def droids(_):
    print("These aren't the droids you're looking for.")


@app.subcommand([arg("number", type=int)])
def square(args):
    print(args.number**2)


app.main()
