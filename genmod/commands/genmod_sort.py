#!/usr/bin/env python
# encoding: utf-8
"""
genmod_sort.py

Command line tool for sorting variants with genmod.

Created by Måns Magnusson on 2015-08-21.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""

from __future__ import print_function

import sys
import os
<<<<<<< HEAD
import logging

import click

=======
import click
import logging
>>>>>>> feature/fix_compounds_single

from codecs import open
from tempfile import NamedTemporaryFile

<<<<<<< HEAD
from genmod.utils import (print_variants, print_variant_for_sorting, 
                          sort_variants)
=======
# from genmod import (sort_variants, print_headers)
from genmod.vcf_tools import (print_variant_for_sorting, sort_variants, 
get_info_dict, print_variant, HeaderParser, print_headers)

from genmod.utils import (get_chromosome_priority, get_rank_score)

>>>>>>> feature/fix_compounds_single

@click.command()
@click.argument('variant_file', 
                    nargs=1, 
                    type=click.File('rb'),
                    metavar='<vcf_file> or -'
)
@click.option('-o', '--outfile', 
<<<<<<< HEAD
                    type=click.Path(exists=False),
                    help='Specify the path to a file where results should be stored.'
)
@click.option('-f', '--family_id', 
                    help="Specify the family id for sorting. If no family id "\
                    "the first family found in annotation will be used."
)
@click.option('-v', '--verbose', 
                count=True,
                help='Increase output verbosity.'
)
def sort(variant_file, outfile, family_id, verbose):
    """
    Sort a VCF file based on rank score.\n
    """
    from genmod.log import init_log, LEVELS
    from genmod import logger as root_logger 
    loglevel = LEVELS.get(min(verbose,2), "WARNING")
    init_log(root_logger, loglevel=loglevel)
    
    logger = logging.getLogger(__name__)
    
    #Save the variant lines for printing
    header_lines = []
    
=======
                    type=click.File('w'),
                    help='Specify the path to a file where results should be stored.'
)
@click.option('-f', '--family_id', 
                    help='Specify the family id for sorting.'
)
@click.option('-s', '--silent',
                is_flag=True,
                help='Do not print the variants.'
)
@click.option('-p', '--position',
                is_flag=True,
                help='If variants should be sorted by position.'
)
def sort(variant_file, outfile, family_id, silent, position):
    """
    Sort a VCF file based on rank score.
    """    
    logger = logging.getLogger(__name__)
    head = HeaderParser()

>>>>>>> feature/fix_compounds_single
    # Create a temporary variant file for sorting
    temp_file = NamedTemporaryFile(delete=False)
    temp_file.close()
    # Open the temp file with codecs
    temp_file_handle = open(
                                temp_file.name,
                                mode='w',
                                encoding='utf-8',
                                errors='replace'
                                )
    
    # Print the variants with rank score in first column
    for line in variant_file:
        line = line.rstrip()
        if line.startswith('#'):
<<<<<<< HEAD
            header_lines.append(line)
        else:
            print_variant_for_sorting(
                variant_line = line, 
                outfile = temp_file_handle,
                family_id = family_id
            )
    # The tempfile includes the unsorted variants
    temp_file_handle.close()
    
    # Sort the variants based on rank score
    sort_variants(
        infile = temp_file.name, 
        mode='rank'
    )
    
    # Print the headers
    if outfile:
        g = open(outfile, 'w', encoding='utf-8')
    
    for header in header_lines:
        if outfile:
            g.write(header + '\n')
        else:
            print(header)
    if outfile:
        g.close()
    
    # Print the variants
    print_variants(
        variant_file = temp_file.name,
        outfile = outfile,
        mode = 'modified'
    )
=======
            if line.startswith('##'):
                head.parse_meta_data(line)
            else:
                head.parse_header_line(line)
        else:
            priority = '0'
            
            if position:
                chrom = line.split()[0]
                priority = get_chromosome_priority(chrom)
            else:
                priority = get_rank_score(line)
            
            print_variant_for_sorting(
                variant_line=line, 
                priority=priority,
                outfile = temp_file_handle,
            )
    
    temp_file_handle.close()
    
    sort_mode = 'rank'
    if position:
        sort_mode = 'chromosome'
    # Sort the variants based on rank score
    sort_variants(
        infile = temp_file.name, 
        mode=sort_mode
    )
    
    # Print the headers
    print_headers(
        head = head, 
        outfile = outfile, 
        silent=silent
    )
    
    # Print the variants
    with open(temp_file.name, mode='r', encoding='utf-8', errors='replace') as f:
        for variant_line in f:
            print_variant(
                variant_line = variant_line, 
                outfile = outfile, 
                mode = 'modified',
                silent=False
                )
>>>>>>> feature/fix_compounds_single
    
    logger.info("Removing temp file")
    os.remove(temp_file.name)
    logger.debug("Temp file removed")
    


if __name__ == '__main__':
    sort()