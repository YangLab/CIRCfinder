#!/usr/bin/env python
import sys
import re
import string


def main():
    if len(sys.argv) != 3:
        print('boundary_read_summary.py intron.fa read_fold')
        sys.exit(0)
    with open('boundary_read.txt', 'w') as outf:
        with open(sys.argv[1], 'r') as intron:
            for line in intron:
                if line.startswith('>'):
                    head = line[1:-1]
                    print('deal with ' + head)
                else:
                    boundary_read = extract_boundary_read(head, sys.argv[2])
                    if boundary_read:
                        outf.write(head + '\n')
                        outf.write(line[:100] + ' ' * 5 + line[-101:])
                        for read in boundary_read:
                            outf.write(read[0])
                            outf.write(' ' * (205 - len(read[0]) - read[1]))
                            outf.write(read[2] + '\n')


def extract_boundary_read(head, fold):
    read = []
    s = re.split(r':|-|\|', head)[1]
    e = re.split(r':|-|\|', head)[2]
    length = int(e) - int(s)
    i = 'unmapped'
    end_index_0 = {}
    end_index_16 = {}
    with open(fold + '/' + head + '_read_end_' + i + '.sam', 'r') as end:
        for line in end:
            if not line.startswith('@') and line.split()[3] == '1':
                if line.split()[1] == '0':
                    end_index_0[line.split()[0]] = line.split()[9]
                elif line.split()[1] == '16':
                    end_index_16[line.split()[0]] = line.split()[9]
    with open(fold + '/' + head + '_read_start_' + i + '.sam', 'r') as start:
        for line in start:
            if not line.startswith('@'):
                if line.split()[1] == '0' and line.split()[0] in end_index_0:
                    n = length - int(line.split()[3]) + 1
                    if n >= 100:
                        continue
                    start_seq = end_index_0[line.split()[0]]
                    end_seq = line.split()[9]
                    read.append([start_seq, n, end_seq])
                elif (line.split()[1] == '16' and
                        line.split()[0] in end_index_16):
                    n = length - int(line.split()[3]) + 1
                    if n >= 100:
                        continue
                    start_seq = end_index_16[line.split()[0]]
                    end_seq = line.split()[9]
                    read.append([start_seq, n, end_seq])
    return read


if __name__ == '__main__':
    main()
