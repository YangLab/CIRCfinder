CIRCfinder
==========

CIRCfinder is a pipeline to map junction reads for circular intronic RNAs
(ciRNAs). Using this pipeline, you could determine the exact boundaries of
interested ciRNAs, so that you could do further characterizations for them.

A schematic flow shows the pipeline
-----------------------------------

![pipeline](http://www.picb.ac.cn/rnomics/data/resources/circfinder.jpg)

Features
--------

* Not specific to certain cell line/tissue/species
* Not specific to certain RNA-seq technology (length/sequencing platform)
* Effective and efficient to map junction reads

Usage
-----

```bash
usage: CIRCfinder.py [-h] [-v] --intron_region INTRON --tophat_folder FOLDER
                     [--out_folder OUT] [--debug] [--length LENGTH]

Pipeline to map junction reads for ciRNAs

optional arguments:
-h, --help            show this help message and exit
-v                    show program's version number and exit
--intron_region INTRON see example file in test folder
--tophat_folder FOLDER
--out_folder OUT
--debug
--length LENGTH read length, default: 100
```
*Please add the CIRCfinder directory to your $PATH first. You could find examples in the test folder*

Results
-------

You should get result file boundary_read.txt under the CIRCfinder_out folder by
default. In addition, you could also run run_test.sh under the test folder to
carry out the whole analysis on example data.

Requirements
------------

* Interested intron regions that may contain ciRNAs
* Poly(A)- RNA-seq dataset for your interested cell line/tissue/species (RNase R treatment is recommended)
* [TopHat](http://ccb.jhu.edu/software/tophat/index.shtml)
* [Bowtie](http://bowtie-bio.sourceforge.net/index.shtml)
* [bedtools](https://github.com/arq5x/bedtools2)

Citation
--------

**[Zhang Y, Zhang XO, Chen T, Xiang JF, Yin QF, Xing YH, Zhu S, Yang L and Chen LL. Circular intronic long noncoding RNAs. Mol Cell, 2013, 51:792-806](http://www.cell.com/molecular-cell/abstract/S1097-2765%2813%2900590-X)**

License
-------

Copyright (C) 2014 YangLab.
See the [LICENSE](https://github.com/YangLab/CIRCfinder/blob/master/LICENSE)
file for license rights and limitations (MIT).
