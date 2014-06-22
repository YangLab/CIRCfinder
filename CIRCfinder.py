#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: CIRCfinder.py
Author: Xiao-Ou Zhang
Email: kepbod@gmail.com
Github: https://github.com/kepbod
Description: A pipeline to map junction reads for circular intronic RNAs (ciRNAs)
"""

import sys
import argparse
import os
import os.path
import subprocess
import logging
import shutil
from time import strftime, localtime

def main():
    parser = argparse.ArgumentParser(description='Pipeline to map junction reads for ciRNAs')
    parser.add_argument('-v', action='version', version='%(prog)s 0.1.0')
    parser.add_argument('--intron_region', required=True, dest='intron', help='see example file in test folder')
    parser.add_argument('--tophat_folder', required=True, dest='folder')
    parser.add_argument('--out_folder', dest='out', default='CIRCfinder_out')
    parser.add_argument('--debug', action='store_false', dest='debug')
    parser.add_argument('--length', type=int, default=100, dest='length', help='read length, default: 100')
    options = parser.parse_args()
    if options.debug:
        logging.basicConfig(filename='CIRCfinder.log', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='CIRCfinder.log', level=logging.INFO)
    logging.info('CIRCfinder start at %s' % (strftime('%d %b %Y %H:%M:%S', localtime())))
    CIRCfinder_path = os.path.dirname(os.path.realpath(__file__))
    try:
        os.mkdir('CIRCfinder_out')
    except OSError:
        shutil.rmtree('CIRCfinder_out')
        os.mkdir('CIRCfinder_out')
    os.mkdir('CIRCfinder_out/read')
    os.mkdir('CIRCfinder_out/intron')
    os.mkdir('CIRCfinder_out/mapping')
    pwd = os.getcwd()
    options.folder = pwd + '/' + options.folder
    options.intron = pwd + '/' + options.intron
    os.chdir('CIRCfinder_out')
    logging.info('Convert unmapped reads from bam to fastq at %s' % (strftime('%d %b %Y %H:%M:%S', localtime())))
    logging.debug('bamToFastq -i %s/unmapped.bam -fq unmapped.fastq' % options.folder)
    subprocess.call('bamToFastq -i %s/unmapped.bam -fq unmapped.fastq' % options.folder, shell=True)
    logging.info('Extract unmapped sequences and index at %s' % strftime('%d %b %Y %H:%M:%S', localtime()))
    #perl -ane 'BEGIN{print ">index\n"};chomp;print "${_}NNNNNNNNNN\n" if $.%4==2' unmapped.fastq > unmapped.fa'
    with open('unmapped.fastq', 'r') as fq, open('unmapped.fa', 'w') as fa:
        fa.write('>index\n')
        for i, line in enumerate(fq):
            if (i + 1) % 4 == 2:
                fa.write(line[:-1] + 'NNNNNNNNNN\n')
    logging.debug('bowtie-build -f unmapped.fa unmapped')
    subprocess.call('bowtie-build -f unmapped.fa unmapped', shell=True)
    logging.info('Extract anchor sequences from intron regions and map at %s' % strftime('%d %b %Y %H:%M:%S', localtime()))
    #perl -alne '$_= substr $_,0,10 if !/^>/;print' options.intron > intron_anchor.fa
    with open(options.intron, 'r') as intron, open('intron_anchor.fa', 'w') as anchor:
        for line in intron:
            if not line.startswith('>'):
                anchor.write(line[:10] + '\n')
            else:
                anchor.write(line)
    logging.debug('bowtie -v 2 -y --all -p 40 --best -f -S unmapped intron_anchor.fa unmapped.sam')
    subprocess.call('bowtie -v 2 -y --all -p 40 --best -f -S unmapped intron_anchor.fa unmapped.sam', shell=True)
    logging.debug('%s/script/extract_anchor.py unmapped.sam unmapped.fa unmapped %d' % (CIRCfinder_path, options.length))
    subprocess.call('%s/script/extract_anchor.py unmapped.sam unmapped.fa unmapped %d' % (CIRCfinder_path, options.length), shell=True)
    logging.info('index intron sequences at %s' % strftime('%d %b %Y %H:%M:%S', localtime()))
    #perl -alne 'open $out,">intron/",substr($_,1) . ".fa" if /^>/;print $out $_' options.intron
    with open(options.intron, 'r') as intron:
        for line in intron:
            if line.startswith('>'):
                intron_fa = open('intron/' + line[1:-1] + '.fa', 'w')
            intron_fa.write(line)
        intron_fa.close()
    logging.debug('for i in intron/*.fa;do bowtie-build -f $i ${i/.fa/};done')
    subprocess.call('for i in intron/*.fa;do bowtie-build -f $i ${i/.fa/};done', shell=True)
    logging.info('map junction reads as %s' % strftime('%d %b %Y %H:%M:%S', localtime()))
    logging.debug('for i in read/*.fa;do a=${i/read\/};b=${a/_read*/};bowtie -v 3 -y --best -f -S intron/$b $i mapping/${a/.fa/}.sam;done')
    subprocess.call('for i in read/*.fa;do a=${i/read\/};b=${a/_read*/};bowtie -v 3 -y --best -f -S intron/$b $i mapping/${a/.fa/}.sam;done', shell=True)
    logging.debug('%s/script/boundary_read_summary.py %s mapping' % (CIRCfinder_path, options.intron))
    subprocess.call('%s/script/boundary_read_summary.py %s mapping' % (CIRCfinder_path, options.intron), shell=True)
    logging.info('CIRCfinder end at %s' % strftime('%d %b %Y %H:%M:%S', localtime()))

if __name__ == '__main__':
    main()
