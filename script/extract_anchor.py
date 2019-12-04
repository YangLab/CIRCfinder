#!/usr/bin/env python
import sys
import pysam


def main():
    if len(sys.argv) != 5:
        print('extract_anchor.py sam fa i length')
        sys.exit(0)
    i = sys.argv[3]
    length = int(sys.argv[4]) + 10
    flag = ''
    fa = pysam.Fastafile(sys.argv[2])
    with open(sys.argv[1], 'r') as sam:
        for line in sam:
            if not line.startswith('@'):
                label = line.split()[0]  # intron label
                if flag != label:
                    flag = label
                    read_start = open('read/' + label + '_read_start_' + i + '.fa', 'w')
                    read_end = open('read/' + label + '_read_end_' + i + '.fa', 'w')
                pos = int(line.split()[3])
                idx = int(pos / length) * length
                cigar = line.split()[1]
                if cigar == '0':
                    offset = pos % length
                else:
                    offset = pos % length + 10
                seq = fa.fetch('index', idx, idx + length)
                head = '>' + label + '_' + str(idx) + '_' + str(offset)
                head += '_' + cigar + '\n'
                if cigar == '0':
                    read_start.write(head + seq[:(offset - 1)] + '\n')
                    read_end.write(head + seq[(offset - 1):-10] + '\n')
                else:
                    read_end.write(head + seq[:(offset - 1)] + '\n')
                    read_start.write(head + seq[(offset - 1):-10] + '\n')


if __name__ == '__main__':
    main()
