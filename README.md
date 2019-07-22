# arghelp

Helpers for using `argparse`.

## Introduction

Python's `argparse` module out of the box provides a rich set of tools
for building command-line interfaces. While capable, more complex CLIs
including subcommands require a great deal of verbosity; `arghelp` aims
to simplify this.

## Installation

### Installing from source

`arghelp` uses [flit](https://flit.readthedocs.io/en/latest/index.html). With
recent versions of `pip` supprting `pyproject.toml` files simply run 
`pip install .`. Otherwise install flit first and use it to install:

```bash
pip install flit
flit install
```

## Examples

### Simple usage

```python
from arghelp import Application, arg

app = Application([
    arg("-v", "--verbose", action="store_true"),
    arg("name")
])

args = app.parse_args()

greeting = "hello" if args.verbose else "hi"
print(f"{greeting}, {args.name}")
```

Example with output:

    $ python demos/simple_demo.py -v Alex
    hello, Alex
    $ python demos/simple_demo.py Alexa
    hi, Alexa

### Defining a root command

```python
from arghelp import Application, arg


app = Application([
    arg("-v", "--verbose", action="store_true"),
    arg("name")
])

@app.root_command()
def main(args):
    greeting = "hello" if args.verbose else "hi"
    print(f"{greeting}, {args.name}")


app.main()
```

Example with output:

```
$ python demos/simple_with_root.py -v Alexa
hello, Alexa
$ python demos/simple_with_root.py Alex
hi, Alex
```

### Using subcommands

```python
from arghelp import Application, arg


app = Application([
    arg("--verbose", "-v", action="store_true"),
])


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
```

Example with output:

    $ python demos/subcmds.py -v hi Alex
    Hi, Alex! Hi hi hi!
    $ python demos/subcmds.py -v hello Alexa
    Hello, Alexa! How are you today?

### Subcommands and a root command

```python
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
```

Example with output:

    $ python demos/subcmd_with_root.py
    Nothing to see here. Move along!
    $ python demos/subcmd_with_root.py droids
    These aren't the droids you're looking for.
    $ python demos/subcmd_with_root.py square 10
    100

### Mutually exclusive options

Mutually exclusive options are supported via the `Group` class:

```python
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
```

For a complete example, see `demos/groups.py`.
