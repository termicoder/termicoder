#!/bin/bash

# this script compiles the program into an executabe
# define online judge constant
# first argument is the file name
# second argument is the name of executabe to be produced

PRG=$1
OUT=$2
g++ -g -Wall -D ONLINE_JUDGE -o $OUT $PRG
