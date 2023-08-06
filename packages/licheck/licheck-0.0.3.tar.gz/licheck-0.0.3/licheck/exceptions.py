#
# exceptions.py
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
"""Exceptions file."""


class BinaryDoesNotExist(Exception):
    r"""Binary Does Not Exist."""


class InvalidConfiguration(Exception):
    r"""Invalid Configuration."""


class InvalidCache(Exception):
    r"""Invalid Cache."""


class InvalidOutput(Exception):
    r"""The output from an external process in unexpected."""


class InvalidCommonDataStructure(Exception):
    r"""Invalid Common Data Structure."""


class IncoherentProgrammingLanguageValue(Exception):
    r"""The programming language value is not uniform."""
