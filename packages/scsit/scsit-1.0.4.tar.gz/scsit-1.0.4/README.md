### Introduction

scsit: A high-efficiency cell types identification tool for single-cell sequencing data from SPLiT-seq

#### Eg: 
```
  Program: scsit (A high-efficiency preprocessing tool for single-cell sequencing data from SPLiT-seq)
  
  Contact: Shangqian Xie <sqianxie@foxmail.com>
    Usage: scsit [options] -r1 input_r1.fastq -r2 input_r2.fastq -p primer.list -b barcode.list -o output
    
  params:
    "   -r1 R1File        Paths to files that contain input read1 of SPLiT-seq pair-end files
    "   -r2 R2File        Paths to files that contain input read2 of SPLiT-seq pair-end files
    "   -p primerList     Primer list of all oligonucleotide sequences used
    "   -b barcodeList    The 96 well plate oligonucleotides used for each round of barcodes
    Options:
    "   -t int            Maximum number of threads to use [default:4]
    "   -o output_prefix  Paths to files that contain output file prefix [default:output]
    "   -h                show this help message and exit
```