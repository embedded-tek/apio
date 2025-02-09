# -*- coding: utf-8 -*-
# -- This file is part of the Apio project
# -- (C) 2016-2024 FPGAwars
# -- Authors
# --  * Jesús Arroyo (2016-2019)
# --  * Juan Gonzalez (obijuan) (2019-2024)
# -- Licence GPLv2
"""Main implementation of APIO UNINSTALL command"""

from pathlib import Path
import click
from apio.managers.installer import Installer, list_packages
from apio.profile import Profile
from apio import util
from apio.resources import Resources
from apio.commands import options


def _uninstall(packages: list, platform: str, resources: Resources):
    """Uninstall the given list of packages"""

    # -- Ask the user for confirmation
    if click.confirm("Do you want to continue?"):

        # -- Uninstall packages, one by one
        for package in packages:

            # -- The uninstalation is performed by the Installer object
            modifiers = Installer.Modifiers(force=False, checkversion=False)
            installer = Installer(package, platform, resources, modifiers)

            # -- Uninstall the package!
            installer.uninstall()

    # -- User quit!
    else:
        click.secho("Abort!", fg="red")


# ---------------------------
# -- COMMAND
# ---------------------------
# R0913: Too many arguments (6/5)
# pylint: disable=R0913
@click.command("uninstall", context_settings=util.context_settings())
@click.pass_context
@click.argument("packages", nargs=-1)
@options.project_dir_option
@options.all_option_gen(help="Uninstall all packages.")
@options.list_option_gen(help="List all installed packages.")
@options.platform_option
def cli(
    ctx,
    # Arguments
    packages,
    # Options
    project_dir: Path,
    all_: bool,
    list_: bool,
    platform: str,
):
    """Uninstall packages."""

    # -- Load the resources.
    resources = Resources(platform=platform, project_dir=project_dir)

    # -- Uninstall the given apio packages
    if packages:
        _uninstall(packages, platform, resources)

    # -- Uninstall all the packages
    elif all_:

        # -- Get all the installed apio packages
        packages = Profile().packages

        # -- Uninstall them!
        _uninstall(packages, platform, resources)

    # -- List all the packages (installed or not)
    elif list_:
        list_packages(platform)

    # -- Invalid option. Just show the help
    else:
        click.secho(ctx.get_help())
