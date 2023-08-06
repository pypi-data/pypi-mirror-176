#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Decodes DEC-Tec sequences based on a provided ID.

Example:
     decode -a 15954
     decode -s 2143
     decode -d 662

"""

import os
import sys
import argparse

import cmder


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0].strip())
    parser.add_argument('-a', '--analysis-id', help='Analysis ID identifies a decoding sample.', type=int)
    parser.add_argument('-s', '--selection-id', help='Selection ID identifies a series of decoding samples.', type=int)
    parser.add_argument('-d', '--decoding-id', help='Decoding ID identifies a series of decoding samples.', type=int)
    parser.add_argument('-o', '--outdir', help='Path to output directory.')
    parser.add_argument('-t', '--tmpdir', help='Path to temporary directory, default: %(default)s', default='/tmp')
    parser.add_argument('-c', '--credential-json', help='JSON file contains database credentials.', type=cmder.filename)
    parser.add_argument('-e', '--experiment-json', help='JSON file describes all experiments.', type=cmder.filename)
    parser.add_argument('-l', '--library-json', help='JSON file describes all libraries.', type=cmder.filename)
    parser.add_argument('-x', '--link-json', help='JSON file describes all sequence file links.', type=cmder.filename)
    parser.add_argument('-n', '--num-cpus', type=int, default=1,
                        help='Number of CPUs can be used for parallelism, default: %(default)s.')
    parser.add_argument('-N', '--num-seqs', type=int, default=100000,
                        help='Number of sequences will be processed in each FASTA file, default: %(default)s.')
    parser.add_argument('-k', '--keep-tmp', action='store_true',
                        help='Flag that will keep temporary directory and intermedia files un-deleted.')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Flag that will ignore the current status and force re-decoding.')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Flag that will invoke quiet mode and output less log messages.')
    parser.add_argument('-D', '--dry_run', help='Only print out tasks and commands without actually running them.',
                        action='store_true')

    args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    if args.analysis_id:
        pass
    elif args.selection_id:
        pass
    elif args.decoding_id:
        pass
    else:
        cmder.logger.error('None of analysis, selection, nor decoding ID was provided, cannot continue!')
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
