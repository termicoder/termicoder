#!/bin/bash
# this script runs PRG with reading from infile and writing to outfile
# USAGE . run.sh <binary file name> <infile> <outfile>

code=$1

(python2 $code)
