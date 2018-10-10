from arghelp import Application, arg

app = Application([
    arg("-v", "--verbose", action="store_true"),
    arg("name")
])

args = app.parse_args()

greeting = "hello" if args.verbose else "hi"
print(f"{greeting}, {args.name}")
