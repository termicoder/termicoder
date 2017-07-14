#!/bin/bash
# this script runs PRG with reading from infile and writing to outfile
# USAGE . run.sh <binary file name> <infile> <outfile>

PRG=$1
infile=$2
outfile=$3

(./$PRG < $infile > $outfile)
