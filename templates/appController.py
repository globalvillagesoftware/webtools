#!/usr/bin/env python3.8
"""
{{ shortProgramDescription }}

{{ programDescription }}

@author:     {{ programAuthor }}

@copyright:  {{ generateYear() }} {{ publisher }}. All rights reserved.

@license:    {{ programLicenceName }}

@contact:    {{ publisherContact }}
@deffield    updated: Updated
"""

import sys
import os
from typing import Optional

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

import {{ program_name }}

__all__ = []
__version__ = {{ appVersion }}
__date__ = '2020-08-07'
__updated__ = '2020-08-07'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    """"Generic exception to raise and log different fatal errors."""
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = f'E: {msg}'
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

program_name = None

def main():
    """"Command line options."""

    program_name = os.path.basename(sys.argv[0])
    program_version = f'{__version__}'
    program_build_date = str(__updated__)
    program_version_message = f'({program_version})s %s ({program_build_date})'
    program_shortdesc = __import__('__main__').__doc__.split('\n')[1]
    program_license = f"""{program_shortdesc}

  Created by {{ programAuthor }} on {str(__date__)}.
  Copyright {{ generateYear }} {{ copyright}} All rights reserved.

  Licensed {{ programLicence }}

  Distributed on an 'AS IS' basis without warranties
  or conditions of any kind, either express or implied.

"""

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-v',
                            '--verbose',
                            default=None,
                            dest='verbose',
                            action='count',
                            help='set verbosity level [default: None')
        parser.add_argument('-V', '--version',
                            action='version',
                            version=program_version_message)

        {{ invokeApp() }}
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * ' '
        print(f'{program name}: {repr(e)}',
              file=stderr)
        print(f'{indent}for help use --help',
              file=stderr)
        return 2

if __name__ == '__main__':
    if DEBUG:
        sys.argv.append('-v')
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = f'{program_name}.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open(f'{program_name}_stats.txt', 'wb')
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
