#
# constants.py
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
"""A file that contains all the global constants."""

common_defaults = dict()

common_defaults = {
    'table element max length': 16,
    'cache file': 'cache.yml',
}

programs = dict()
programs['python'] = {
    'binary': 'deplic',
    'program name': 'dep_license',
}

if __name__ == '__main__':
    pass
