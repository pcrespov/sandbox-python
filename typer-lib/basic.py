import typer


def main(username: str, this_is_an_option: bool = typer.Option(True, "--foo")):
    if username == "root":
        print("The root user is reserved")
        raise typer.Exit(code=1)
    print(f"New user created: {username}, {this_is_an_option}")


if __name__ == "__main__":
    typer.run(main)
