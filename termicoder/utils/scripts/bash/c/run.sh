#!/bin/bash
# this script runs PRG with reading from infile and writing to outfile
# USAGE . run.sh <binary file name> <infile> <outfile>

PRG=$1

(./$PRG)
