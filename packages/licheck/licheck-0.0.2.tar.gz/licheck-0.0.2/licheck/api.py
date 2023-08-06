#
# api.py
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
"""The main file."""

import copy
import hashlib
import json
import logging
import pathlib
import re
import shlex
import shutil
import subprocess
from urllib.parse import urlparse

import requests
import yaml
from appdirs import AppDirs
from tabulate import tabulate

from .constants import common_defaults, programs
from .exceptions import (BinaryDoesNotExist,
                         IncoherentProgrammingLanguageValue, InvalidCache,
                         InvalidCommonDataStructure, InvalidConfiguration,
                         InvalidOutput)


def build_command(binary: str, license_program: str, file: str) -> str:
    r"""Build a command to let the license programs discover all packages.

    :parameter binary: the path of the executable binary.
    :parameter license_program: the program name.
    :parameter file: the file name where the licenses need to be checked.
    :type binary: str
    :type license_program: str
    :type file: str
    :returns: the command string
    :rtype: str
    :raises: a built-in exception.
    """
    command = str()
    if license_program == 'dep_license':
        output_format = 'json'
        command = binary + ' --dev --format ' + output_format + ' ' + file

    return command


def create_data_object(input: list, license_program: str, file: str) -> list:
    r"""Create a data structure common to all outputs.

    :parameter input: a list of objects containing the dependencies.
    :parameter license_program: the program name.
    :parameter file: the file name where the licenses need to be checked.
    :type input: list
    :type license_program: str
    :type file: str
    :returns: a list of objects with a common structure in this program.
    :rtype: list
    :raises: a built-in exception.
    """
    output = list()
    if license_program == 'dep_license':
        for element in range(0, len(input)):
            output.append(element)

            output[element] = dict()
            output[element]['package'] = input[element]['Name']

            # This element should be a list of licenses.
            output[element]['license_short'] = [input[element]['Meta']]

            # This element should be a list of licenses.
            output[element]['license_long'] = [input[element]['Classifier']]

            # Add the file name.
            output[element]['file'] = file
            output[element]['version'] = str()

    return output


def get_data(command: str, license_program: str) -> dict:
    r"""Run a command to gen an object with the output of the licenses.

    :parameter command: the command string executed by the shell.
    :parameter license_program: the program name.
    :type input: list
    :type license_program: str
    :returns: an object with a specific structure depending from license_program.
    :rtype: dict
    :raises: InvalidOutput or a built-in exception.
    """
    output = str()

    p = subprocess.run(
        shlex.split(command),
        capture_output=True,
        check=True
    )
    output = p.stdout.decode('UTF-8').strip()

    data = dict()
    if license_program == 'dep_license':
        # Output must conform.
        if not re.match('(Found dependencies: \\d+|no dependencies found)', output):
            raise InvalidOutput

        # Sanitize output so json can be loaded without problems.
        output = re.sub('Found dependencies: \\d+', '', output)
        output = re.sub('no dependencies found', '{}', output)
        data = json.loads(output)

    return data


def transform_cache_to_data_object(cache: dict, file: str, file_checksum: str) -> list:
    r"""Given the cache data structure, transform it into the one used in this program.

    :parameter cache: an object representing the cache.
    :parameter file: the file name.
    :parameter file_checksum: the SHA-512 checksum of the file content.
    :type cache: dict
    :type file: str
    :type file_checksum: str
    :returns: a list of objects with a common structure in this program.
    :rtype: dict
    :raises: a built-in exception.
    """
    if not check_cache_structure(cache):
        raise InvalidCache

    i = 0
    output = list()
    for file_id in cache:
        if file_checksum == file_id:
            x = 0
            while x < len(cache[file_id]):
                output.append(dict())

                output[i]['package'] = cache[file_id][x]['p']

                # This element should be a list of licenses.
                output[i]['license_short'] = cache[file_id][x]['s']

                # This element should be a list of licenses.
                output[i]['license_long'] = cache[file_id][x]['l']

                # Add the file name.
                output[i]['file'] = file

                output[i]['version'] = cache[file_id][x]['v']

                x += 1
                i += 1

    return output


def read_yaml_file(file: str) -> dict:
    r"""Read a YAML file and load the object.

    :parameter file: the file name.
    :type file: str
    :returns: an objects.
    :rtype: dict
    :raises: a PyYAML or a built-in exception.
    """
    data = dict()
    if pathlib.Path(file).is_file():
        data = yaml.load(open(file, 'r'), Loader=yaml.SafeLoader)

    return data


def write_cache(packages: list, file_checksum: str, cache_file: str):
    r"""Write an object as a YAML file.

    :parameter packages: an object with a common structure in this program.
    :parameter file_checksum: the SHA-512 checksum of the file content.
    :parameter cache_file: the file where to write the output
    :type packages: list
    :type file_checksum: str
    :type cache_file: str
    :raises: a PyYAML or a built-in exception.
    """
    if not check_data_object_structure(packages):
        raise InvalidCommonDataStructure

    table = dict()
    table[file_checksum] = list()
    for package in packages:
        table[file_checksum].append({
            'p': package['package'],
            's': package['license_short'],
            'l': package['license_long'],
            'v': package['version'],
        })

    # Write one file at the time using the append operation.
    with open(cache_file, 'a') as f:
        f.write(yaml.dump(table))


def check_licenses(packages: list, licenses_allowed: list, include_empty_as_errors: bool = True) -> list:
    r"""Filter packages to include only the ones with errors.

    :parameter packages: an object with a common structure in this program.
    :parameter licenses_allowed: the file name.
    :parameter include_empty_as_errors: if set to ``True`` add a package
        to the error list if the ``license_long`` attribute is empty.
        Defaults to ``True``.
    :type packages: list
    :type licenses_allowed: list
    :type include_empty_as_errors: bool
    :returns: a sublist of ``packages`` containing the invalid packages.
    :rtype: list
    :raises: a built-in exception.
    """
    if not check_data_object_structure(packages):
        raise InvalidCommonDataStructure
    for license in licenses_allowed:
        if not isinstance(license, str):
            raise TypeError

    errors = list()

    for package in packages:
        for p in package['license_long']:
            if p not in licenses_allowed:
                errors.append(package)
        if include_empty_as_errors and len(package['license_long']) == 0:
            errors.append(package)

    return errors


def prepare_print(packages: list, cut_output: bool = False) -> list:
    r"""Re-format the output.

    :parameter packages: an object with a common structure in this program.
    :parameter cut_output: if set to ``True`` license colums are cut.
        Defaults to ``True``.
    :type packages: list
    :type cut_output: bool
    :returns: an edited copy ``packages``.
    :rtype: list
    :raises: a built-in exception.
    """
    if not check_data_object_structure(packages):
        raise InvalidCommonDataStructure

    final_output = copy.deepcopy(packages)

    j = 0
    while cut_output and j < len(packages):
        i = 0
        for x in packages[j]['license_short']:
            if cut_output and len(x) > common_defaults['table element max length']:
                final_output[j]['license_short'][i] = x[:common_defaults['table element max length']] + '...'
            i += 1
        i = 0
        for x in packages[j]['license_long']:
            if cut_output and len(x) > common_defaults['table element max length']:
                final_output[j]['license_long'][i] = x[:common_defaults['table element max length']] + '...'
            i += 1
        j += 1

    # Fill empty colums.
    while j < len(packages):
        if packages[j]['version'] == str():
            final_output[j]['version'] = '-'
        j += 1

    return final_output


def print_errors(packages: list):
    r"""Print the packages with errors.

    :parameter packages: an object with a common structure in this program.
    :type packages: list
    :raises: a built-in exception.
    """
    if not check_data_object_structure(packages):
        raise InvalidCommonDataStructure

    if len(packages) > 0:
        logging.basicConfig(format='INFO:licheck:\n%(message)s', level=logging.INFO)
        logging.info('unapproved licenses')
        logging.info(tabulate(packages, headers="keys"))


def get_binary_and_program(language: str) -> tuple:
    r"""Get the license binary path and the program name.

    :parameter language: the name of a programming language.
    :type language: str
    :returns: a tuple containing the binary and the program name
        of the license program.
    :rtype: tuple
    :raises: a BinaryDoesNotExist or a built-in exception.
    """
    binary = str()
    program_name = str()

    if language in programs:
        binary = programs[language]['binary']
        program_name = programs[language]['program name']

    if shutil.which(binary) is None:
        raise BinaryDoesNotExist
    else:
        return shutil.which(binary), program_name


def check_configuration_structure(configuration: dict, local: bool = True) -> bool:
    r"""Check the configuration file data structure.

    :parameter configuration: an object containing the configuration.
    :parameter local: if ``True`` assert local configurations.
    :type data_struct: dict
    :type local: bool
    :returns: ``True`` if the configuration is valid, ``False`` otherwise.
    :rtype: bool
    :raises: a built-in exception.
    """
    ok = False

    if local:
        if ('language' in configuration
           and isinstance(configuration['language'], str)
           and len(configuration['language']) > 0
           and 'include' in configuration
           and isinstance(configuration['include'], list)
           and 'files to check' in configuration
           and isinstance(configuration['files to check'], list)
           and len(configuration['files to check']) > 0
           and 'allowed licenses' in configuration
           and isinstance(configuration['allowed licenses'], list)):
            ok = True
            for f in configuration['files to check']:
                if not isinstance(f, str):
                    ok = False
            if ok:
                for f in configuration['include']:
                    if not isinstance(f, str):
                        ok = False
            if ok:
                for url in configuration['include']:
                    # Only use HTTPS.
                    if urlparse(url).scheme not in ['https']:
                        ok = False
    else:
        if ('language' in configuration
           and isinstance(configuration['language'], str)
           and len(configuration['language']) > 0
           and 'include' in configuration
           and isinstance(configuration['include'], list)
           and configuration['include'] == list()
           and 'files to check' in configuration
           and isinstance(configuration['files to check'], list)
           and configuration['files to check'] == list()
           and 'allowed licenses' in configuration
           and isinstance(configuration['allowed licenses'], list)):
            ok = True

    if ok:
        for license in configuration['allowed licenses']:
            if not isinstance(license, str):
                ok = False

    return ok


def check_cache_structure(cache: dict) -> bool:
    r"""Check the cache data structure.

    :parameter cache: an object containing the cache.
    :typecache: dict
    :returns: ``True`` if the cache is valid, ``False`` otherwise.
    :rtype: bool
    :raises: a built-in exception.
    """
    ok = False

    j = 0
    for element in cache:
        if isinstance(cache[element], list):
            i = 0
            for package in cache[element]:
                if (isinstance(package, dict)
                   and 'l' in package
                   and 'p' in package
                   and 's' in package
                   and 'v' in package
                   and isinstance(package['l'], list)
                   and isinstance(package['p'], str)
                   and isinstance(package['s'], list)
                   and isinstance(package['v'], str)
                   and len(package['p']) > 0):
                    ok = True
                    if ok:
                        for license_long in package['l']:
                            if not isinstance(license_long, str):
                                ok = False
                    if ok:
                        for license_short in package['s']:
                            if not isinstance(license_short, str):
                                ok = False
                if ok:
                    i += 1
            if i == len(cache[element]):
                j += 1

    # An empty cache is a valid cache.
    if j == len(cache) or cache == dict():
        ok = True

    return ok


def check_data_object_structure(data: list) -> bool:
    r"""Check the common data structure.

    :parameter data: a list with a common structure in this program.
    :type data: list
    :returns: ``True`` if the cache is valid, ``False`` otherwise.
    :rtype: list
    :raises: a built-in exception.
    """
    ok = False
    in_loop = False
    go = False

    i = 0
    for d in data:
        in_loop = True
        if (isinstance(d, dict)
           and 'package' in d
           and 'license_short' in d
           and 'license_long' in d
           and 'file' in d
           and 'version' in d
           and isinstance(d['package'], str)
           and isinstance(d['license_short'], list)
           and isinstance(d['license_long'], list)
           and isinstance(d['file'], str)
           and isinstance(d['version'], str)
           and len(d['package']) > 0
           and len(d['file']) > 0):
            j = 0
            go = False
            for license_short in d['license_short']:
                if isinstance(license_short, str):
                    j += 1
            if j == len(d['license_short']):
                j = 0
                for license_long in d['license_long']:
                    if isinstance(license_long, str):
                        j += 1
                if j == len(d['license_long']):
                    go = True

            if go:
                i += 1

    if (not in_loop and i == 0) or i == len(data):
        ok = True

    return ok


def read_configuration_file(file: str, local: bool = True) -> tuple:
    r"""Read the configuration file.

    :parameter file: the file name of the configuration file.
    :parameter local: the file name.
    :type file: str
    :type local: bool
    :returns: a tuple with the data fields.
    :rtype: tuple
    :raises: InvalidConfiguration or a built-in exception.
    """
    configuration = read_yaml_file(file)
    if not check_configuration_structure(configuration, local):
        raise InvalidConfiguration

    return (
        configuration['allowed licenses'],
        configuration['files to check'],
        configuration['language'],
        configuration['include'],
    )


def read_cache_file(file: str) -> dict:
    r"""Read the cache file.

    :parameter file: the path of the cache file.
    :type file: str
    :returns: an object containing the cache.
    :rtype: dict
    :raises: InvalidCache or a built-in exception.
    """
    cache = read_yaml_file(file)
    if not check_cache_structure(cache):
        raise InvalidCache

    return cache


def read_remote_files(include_files: list, cache_dir: str) -> list:
    r"""Get the list of allowed licenses from remote files.

    :parameter include_files: a list of URLs of configuration files.
    :parameter cache_dir: the directory where all the cache files lie.
    :type include_files: list
    :type cache_dir: str
    :returns: a list of allowed licenses.
    :rtype: list
    :raises: IncoherentProgrammingLanguageValue or a built-in exception.
    """
    for include in include_files:
        if not isinstance(include, str):
            raise TypeError

    allowed_lic = list()
    language_prev = str()
    i = 0
    for include in include_files:
        checksum = hashlib.sha512(include.encode('UTF-8')).hexdigest()
        checksum += '.yml'
        full_path = pathlib.Path(cache_dir, checksum)
        if not full_path.is_file():
            # Cache files locally.
            r = requests.get(include)
            with open(full_path, 'wb') as f:
                f.write(r.content)

        allowed_licenses, dependencies_files, language, include = read_configuration_file(full_path, local=False)
        allowed_lic += allowed_licenses

        if i > 0 and language != language_prev:
            raise IncoherentProgrammingLanguageValue

        i += 1

        language_prev = language

    # Avoid duplicate elements.
    return list(set(allowed_lic))


def create_dependencies_files_data_structure(dependencies_files: list) -> dict:
    r"""Create an object that couples file names and checksums.

    :parameter dependencies_files: a list of files containing the dependencies to be checked.
    :type packages: list
    :returns: an object with keys the file names and values their checksum.
    :rtype: dict
    :raises: a built-in exception.
    """
    for f in dependencies_files:
        if not isinstance(f, str):
            raise TypeError

    files_struct = dict()
    # Compute the file checksum as a means to check
    # if to go through the download of the metadata
    # the next run.
    for f in dependencies_files:
        full_path_file = str(pathlib.Path(f).absolute())
        file_checksum = hashlib.sha512(open(full_path_file, "rb").read()).hexdigest()
        files_struct[f] = file_checksum

    return files_struct


def pipeline(configuration_file: str = '.allowed_licenses.yml',
             clear_cache: bool = False,
             cut_table_output: bool = False):
    r"""Run the pipeline.

    :parameter configuration_file: the path of the configuration file.
    :parameter clear_cache: if set to ``True`` remove the cache directory.
        Defaults to ``True``.
    :parameter cut_table_output: if set to ``True`` license colums are cut.
        Defaults to ``True``.
    :type configuration_file: str
    :type clear_cache: bool
    :type cut_table_output: bool
    :raises: a built-in exception.
    """
    dirs = AppDirs('licheck')

    # Handle the cache.
    cache_dir = dirs.user_cache_dir
    if clear_cache:
        shutil.rmtree(cache_dir, ignore_errors=True)
    pathlib.Path(cache_dir).mkdir(mode=0o700, exist_ok=True)
    cache_file = str(pathlib.Path(dirs.user_cache_dir, common_defaults['cache file']))
    cache = read_cache_file(cache_file)

    # Read the configuration file.
    allowed_licenses, dependencies_files, language, include = read_configuration_file(configuration_file, local=True)

    # Load remote files.
    allowed_licenses += read_remote_files(include, cache_dir)
    allowed_licenses = set(allowed_licenses)

    files_struct = create_dependencies_files_data_structure(dependencies_files)
    full_list = list()
    out = list()
    i = 0
    # Go through the files with the package dependencies.
    for file in files_struct:
        # Load data from cache or call an external program.
        if files_struct[file] in cache:
            output = transform_cache_to_data_object(cache, file, files_struct[file])
        else:
            binary, program = get_binary_and_program(language)
            command = build_command(binary, program, file)
            data = get_data(command, program)
            output = create_data_object(data, program, file)
        full_list += output
        out.append(output)

        i += 1

    # Remove the cache file since we need to write it again
    # with updated data.
    if pathlib.Path(cache_file).is_file():
        pathlib.Path(cache_file).unlink()

    i = 0
    for file in files_struct:
        write_cache(out[i], files_struct[file], cache_file)
        i += 1

    errors = check_licenses(full_list, allowed_licenses)
    if len(errors) > 0:
        print_errors(prepare_print(errors, cut_table_output))


if __name__ == '__main__':
    pass
