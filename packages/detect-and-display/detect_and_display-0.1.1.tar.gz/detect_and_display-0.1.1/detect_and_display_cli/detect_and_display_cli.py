import os
import sys
import click
import logging

from pathlib import Path

from detect_and_display.utils.detect_and_display_logger import DetectAndDisplayLogger
from detect_and_display import DetectAndDisplay


CONTEXT_SETTINGS = dict(auto_envvar_prefix='DETECTANDDISPLAY')


class Context(object):

    def __init__(self):
        self.verbose = False
        self.config_dir = str(Path.home())
        self.service = None
        self.logger = DetectAndDisplayLogger().get_logger()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)
    
    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'commands'))


class DetectAndDisplayCLI(click.MultiCommand):

    def list_commands(self, ctx):
        commands = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith('.py') and filename.startswith('cmd_'):
                commands.append(filename[4:-3])
        commands.sort()
        return commands

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode('ascii', 'replace')
            mod = __import__(f'detect_and_display_cli.commands.cmd_{name}', None, None, ['cli'])
        except ImportError as err:
            DetectAndDisplayLogger().get_logger().error(err)
            return
        return mod.cli


@click.command(cls=DetectAndDisplayCLI, context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', is_flag=True, default=False, help='Enables verbose mode.')
@pass_context
def cli(ctx, verbose):
    """DetectAndDisplay command line interface."""
    if verbose is False:
        ctx.logger.setLevel(logging.NOTSET)
    else:
        ctx.logger.setLevel(logging.INFO)
    
    ctx.service = DetectAndDisplay()