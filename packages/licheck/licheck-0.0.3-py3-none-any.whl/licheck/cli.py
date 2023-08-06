#
# cli.py
#
# Copyright (C) 2021 frnmst (Franco Masotti) <franco.masotti@tutanota.com>
#
# This file is part of licheck.
#
# licheck is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# licheck is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with licheck.  If not, see <http://www.gnu.org/licenses/>.
#
"""Command line interface file."""

import argparse
import textwrap

from pkg_resources import DistributionNotFound, get_distribution

from .api import pipeline

PROGRAM_DESCRIPTION = 'License check: A frontend to check\nthe licenses of software dependencies.'
VERSION_NAME = 'licheck'
try:
    VERSION_NUMBER = str(get_distribution('licheck').version)
except DistributionNotFound:
    VERSION_NUMBER = 'vDevel'
VERSION_COPYRIGHT = 'Copyright (C) 2021 Franco Masotti, frnmst'
VERSION_LICENSE = 'License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.'
RETURN_VALUES = 'Return values: 0 ok, 1 error, 2 invalid command'
PROGRAM_EPILOG = RETURN_VALUES + '\n\n' + VERSION_COPYRIGHT + '\n' + VERSION_LICENSE


class CliToApi():
    """An interface between the CLI and API functions."""

    def run_pipeline(self, args):
        """Write the table of contents."""
        pipeline(args.configuration_file, args.clear_cache, args.cut_table_output)


class CliInterface():
    """The interface exposed to the final user."""

    def __init__(self):
        """Set the parser variable that will be used instead of using create_parser."""
        self.parser = self.create_parser()

    def create_parser(self):
        """Create the CLI parser."""
        parser = argparse.ArgumentParser(
            description=PROGRAM_DESCRIPTION,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent(PROGRAM_EPILOG))

        parser.add_argument(
            '-c',
            '--configuration-file',
            metavar='CONFIGURATION_FILE',
            default='.allowed_licenses.yml',
            help='configuration file')
        parser.add_argument(
            '-l',
            '--clear-cache',
            action='store_true',
            help='clear all the cache')
        parser.add_argument(
            '-t',
            '--cut-table-output',
            action='store_true',
            help='limit the number of characters of the license columns in the summary table')
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=VERSION_NAME + ' ' + VERSION_NUMBER)

        parser.set_defaults(func=CliToApi().run_pipeline)

        return parser
