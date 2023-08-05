import click

from detect_and_display_cli.detect_and_display_cli import pass_context


@click.group()
@click.version_option()
def cli():
    """Manages Display."""

@cli.command('display')
@click.argument('text_input')
@pass_context
def display(ctx, text_input):
    """Display text into screen."""
    ctx.log(ctx.service.display(text_input))