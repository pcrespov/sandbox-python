import click
from pathlib import Path

@click.group()
def cli():
    pass

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.command()
def dropdb():
    click.echo('Dropped the database')


@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
@click.option("--file", type=Path)
def hello(count, name, filepath):
    for x in range(count):
        click.echo(f"Hello {name} {filepath}!")


cli.add_command(initdb)
cli.add_command(dropdb)
cli.add_command(hello)


if __name__ == "__main__":
    cli()